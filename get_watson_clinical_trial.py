#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import cgi


def find_text(key, dict):
    text = ""
    if dict.has_key(key):
        text = dict[key]

    return text



def get_ct_json(json_dict, drug):

    obj = {}

    nctid_arr = []
    if json_dict.has_key("Relations"):
        if json_dict["Relations"].has_key("GeneVariantEvidenceLevels"):
            gvel_list = json_dict["Relations"]["GeneVariantEvidenceLevels"]
            for gvel in gvel_list:
                drugname = gvel["DrugName"]
                if drugname == drug:
                    if gvel.has_key("ClinicalTrials"):
                        for nctid in gvel["ClinicalTrials"]["NCTIds"]:
                            nctid_arr.append(nctid)


    if json_dict.has_key("ClinicalTrials"):
        ct_list = json_dict["ClinicalTrials"]

        for ct in ct_list:
            if ct["NCTId"] in nctid_arr:
                obj[ct["NCTId"]] = {}
                obj[ct["NCTId"]]["Title"] = ct["Title"]
                obj[ct["NCTId"]]["Phase"] = ct["Phase"]
                obj[ct["NCTId"]]["RecruitingStatus"] = ct["RecruitingStatus"]
                obj[ct["NCTId"]]["CountryList"] = ct["CountryList"]

    return obj



file_path = "./result/"+sys.argv[1]
drug = sys.argv[2]

result = {}

#file = glob.glob("./wfg_api/output/"+user+"/download/"+serialno+"/"+folder+"/*/*/standard_report.json")[0]

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        result = get_ct_json(json_dict, drug)

    return json.dumps(result)

print main()
