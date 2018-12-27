#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import cgi
import glob


def find_text(key, dict):
    text = ""
    if dict.has_key(key):
        text = dict[key]

    return text


def get_drug_info(json_dict, drug):
    FDA_text = ""
    ATD_text = ""
    Summary = ""
    DRUG_INFO = {
        "drug": drug,
        "FDA_text": "",
        "ATD_text": "",
        "Summary": ""
    }

    if json_dict.has_key("Relations"):
        gvel_list = json_dict["Relations"]["GeneVariantEvidenceLevels"]
        for gvel in gvel_list:
            if gvel.has_key("DrugName"):
                if gvel["DrugName"] != drug:
                    continue

                if gvel.has_key("FdaApprovedConditions"):
                    FDA_text = gvel["FdaApprovedConditions"][0]["FDALabel"]
                    ATD_text = gvel["FdaApprovedConditions"][0]["ApprovedTrialsDescription"]
                    DRUG_INFO["FDA_text"] = FDA_text
                    DRUG_INFO["ATD_text"] = ATD_text

        gdel_list = json_dict["Relations"]["GeneDrugEvidenceLevels"]
        for gdel in gdel_list:
            if gdel.has_key("InvestigationalSameCancerDrugs"):
                for g in gdel["InvestigationalSameCancerDrugs"]:
                    drugs = g["Drugs"]
                    for d in drugs:
                        if d["DrugName"] == drug:
                            Summary = d["Evidences"][0]["Summary"]
                            DRUG_INFO["Summary"] = Summary



    return DRUG_INFO



file_path = "./result/"+sys.argv[1]
drug = sys.argv[2]

#file_path = "./result/miseq.myeloid_panel.20180807/json/3_S3.json"
#drug = "Crenolanib"

result = ""

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        result = get_drug_info(json_dict, drug)

    return json.dumps(result)

print main()
