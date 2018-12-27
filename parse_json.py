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

    #print key + "--------------"
    #print text
    return text


def find_list(key, dict):
    list = []
    if dict.has_key(key):
        list = dict[key]

    return list



def roop3(roop_list, TrialPhase, drug_type, DrugName, EvidenceLevel):

    arr = []

    for evi in roop_list:
        Evidence = find_text("Evidence", evi)
        arr.append([drug_type, TrialPhase, DrugName, EvidenceLevel, Evidence])

    return arr



def roop2(roop_list, drug_type, TrialPhase):

    arr = []

    for drugs in roop_list:
        DrugName = find_text("DrugName", drugs)
        EvidenceLevel = find_text("EvidenceLevel", drugs)
        EVI_list = find_list("Evidences", drugs)
        #print "DrugName:"+DrugName

        if len(EVI_list) == 0:
            arr.append([drug_type, TrialPhase, DrugName, EvidenceLevel, ""])
            continue
        else:
            arr.extend(roop3(EVI_list, TrialPhase, drug_type, DrugName, EvidenceLevel))

    return arr



def roop1(roop_list, drug_type):

    arr = []

    for dl in roop_list:
        #print iscd
        TrialPhase = find_text("TrialPhase", dl)
        DRUGS_list = find_list("Drugs", dl)
        #print "TrialPhase:"+str(TrialPhase)
        
        if len(DRUGS_list) == 0:
            arr.append([drug_type, TrialPhase, "", "", ""])
            continue
        else:
            arr.extend(roop2(DRUGS_list, drug_type, TrialPhase))

    return arr



def get_drug_info(json_dict):

    GENE_DRUG = {}

    if json_dict.has_key("Relations"):
        if json_dict["Relations"].has_key("GeneDrugEvidenceLevels"):
            GDEL_list = json_dict["Relations"]["GeneDrugEvidenceLevels"]
            for gdel in GDEL_list:
                GeneName = find_text("GeneName", gdel)
                Invest_same = find_list("InvestigationalSameCancerDrugs", gdel)
                Approve_same = find_list("ApprovedSameCancerDrugs", gdel)
                Approve_other = find_list("ApprovedOtherCancerDrugs", gdel)

                GENE_DRUG[GeneName] = []
                GENE_DRUG[GeneName].extend(roop1(Invest_same, "Invest_same"))
                GENE_DRUG[GeneName].extend(roop2(Approve_same, "Approve_same", ""))
                GENE_DRUG[GeneName].extend(roop2(Approve_other, "Approve_other", ""))
                #print "GeneName:"+GeneName
                #print GENE_DRUG[GeneName]


    #print GENE_DRUG
    return GENE_DRUG




#user = form.getvalue("user", "0")
#caseid = form.getvalue("caseid", "0")
#serialno = form.getvalue("serialno", "0")
#folder = form.getvalue("folder", "0")


file_path = "./result/"+sys.argv[1]
#file_path = "./result/"+form.getvalue("file_path",0)
obj = {}

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        obj = get_drug_info(json_dict)
    
    return json.dumps(obj)

print main()

#print "Content-type: text/plain; charset='utf-8'\n\n"
#print "Content-type: application/json; charset='utf-8'\n\n"
#print json.dumps(obj)
