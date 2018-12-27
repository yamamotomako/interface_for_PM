#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import cgi
import glob


def get_gene_info(json_dict):

    obj = {}

    if json_dict.has_key("Relations"):
        if json_dict["Relations"].has_key("GeneDrugEvidenceLevels"):
            gvel_list = json_dict["Relations"]["GeneDrugEvidenceLevels"]
            for gvel in gvel_list:
                genename = gvel["GeneName"]
                obj[genename] = {
                    "ApprovedSameCancerDrugs": [],
                    "InvestigationalSameCancerDrugs": [],
                    "ApprovedOtherCancerDrugs": []
                }
                if gvel.has_key("ApprovedSameCancerDrugs"):
                    for g in gvel["ApprovedSameCancerDrugs"]:
                        drug_arr = []
                        drug_arr.append(g["DrugName"])
                    obj[genename]["ApprovedSameCancerDrugs"] = drug_arr

                if gvel.has_key("InvestigationalSameCancerDrugs"):
                    for g in gvel["InvestigationalSameCancerDrugs"]:
                        drugs = g["Drugs"]
                        drug_arr = []
                        for d in drugs:
                            drug_arr.append(d["DrugName"])
                        obj[genename]["InvestigationalSameCancerDrugs"] = drug_arr

                if gvel.has_key("ApprovedOtherCancerDrugs"):
                    for g in gvel["ApprovedOtherCancerDrugs"]:
                        drug_arr = []
                        drug_arr.append(g["DrugName"])
                    obj[genename]["ApprovedOtherCancerDrugs"] = drug_arr

    return obj



#file_path = "./result/miseq.myeloid_panel.20180807/json/3_S3.json"
file_path = "./result/"+sys.argv[1]

result = {}

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        result = get_gene_info(json_dict)

    return json.dumps(result)


print main()
