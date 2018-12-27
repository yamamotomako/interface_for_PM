#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import cgi
import glob
import re


def find_text(key, dict):
    text = ""
    if dict.has_key(key):
        text = dict[key]

    return text


def get_drug_info(json_dict):

    DRUG_INFO = {}

    if json_dict.has_key("Drugs"):
        drug_list = json_dict["Drugs"]

        for dl in drug_list:
            DrugName = find_text("DrugName", dl)
            EvidenceLevel = find_text("HighestEvidenceLevel", dl)
            category = find_text("Category", dl)
            status = find_text("ApprovalStatus", dl)
            moa = find_text("MOA", dl)

            DRUG_INFO[DrugName] = [EvidenceLevel, category, status, moa]

            # if json_dict.has_key("Relations"):
            #     gvel_list = json_dict["Relations"]["GeneVariantEvidenceLevels"]
            #     for gvel in gvel_list:
            #         if gvel.has_key("DrugName"):
            #             if gvel["DrugName"] == DrugName:
            #                 if gvel.has_key("FdaApprovedConditions"):
            #                     FDA_text = gvel["FdaApprovedConditions"][0]["FDALabel"]
            #                     ATD_text = gvel["FdaApprovedConditions"][0]["ApprovedTrialsDescription"]
            #                     pa = r"[0-9]{8}"
            #                     f_match = re.findall(pa, FDA_text)
            #                     a_match = re.findall(pa, ATD_text)
            #                     m_match = re.findall(pa, moa)
            #
            #                     DRUG_INFO[gvel["DrugName"]] = [EvidenceLevel, category, status, moa, FDA_text, ATD_text]
            #                     print "----------------"
            #                     print gvel["DrugName"], [EvidenceLevel, category, status, pubmed_str, moa, FDA_text, ATD_text]

    return DRUG_INFO



file_path = "./result/"+sys.argv[1]

#file_path = "./result/miseq.myeloid_panel.20180807/json/3_S3.json"
#drug = "Midostaurin"
#drug = "all"

all_drug = {}

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        all_drug = get_drug_info(json_dict)

    return json.dumps(all_drug)

print main()
