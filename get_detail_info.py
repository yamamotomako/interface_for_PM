#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import commands
import json
import time
import glob
import cgi


reload(sys)
sys.setdefaultencoding('utf8')


def find_text(key, dict):
    text = ""
    if dict.has_key(key):
        text = dict[key]
    return text


HEADER = [
    "sample",
    "Age",
    "Gender",
    "Diagnosis",
    "Chromosome",
    "Position",
    "GENE",
    "VariantId",
    "VariantType",
    "ChromosomeLocationChange",
    "AminoAcid",
    "DNACoding",
    "VUS",
    "MARK",
    "TranscriptId",
    "ClassificationSource",
    "ClassificationEvidence",
    "Effect",
    "AF",
    "DP",
    "log2",
    "level 1",
    "level 2A",
    "level 2B",
    "level 3A",
    "level 3B",
    "level 4",
    "nctid",
    "pmid",
    "Annotation text",
    "Evidence Text",
    "FDA Text"
]

def func(cur_dir,input_folder,result_path,user,date,e_folder):

    log2_dict = {}
    file_obj = glob.glob(input_folder+"/*.log2")

    if len(file_obj) >= 1:
        file = file_obj[0]
        with open(file, "r") as f:
            lines = f.read().rstrip("\n").split("\n")
            for line in lines:
                if line[0] == "#":
                    continue

                data = line.split("\t")
                gene = data[0]
                entrez_id = data[1]
                log2 = data[2]

                log2_dict[gene] = [entrez_id, log2]


    vaf_dict = {}
    file_obj = glob.glob(input_folder+"/*.vcf")

    if len(file_obj) >= 1:
        file = file_obj[0]
        with open(file, "r") as f:
            lines = f.read().rstrip("\n").split("\n")
            for line in lines:
                if line[0] == "#":
                    continue

                data = line.split("\t")
                chr = data[0]
                pos = data[1]
                info = data[7]

                try:
                    r = re.compile('^DP=([0-9]+);')
                    m = r.search(info)
                    dp = m.group(1)
                except:
                    dp = ""

                try:
                    r = re.compile('.+;AF=([0-9|.]+);')
                    m = r.search(info)
                    af = m.group(1)
                except:
                    af = ""

                vaf_dict[chr+"_"+pos] = [dp, af]


    file = glob.glob(cur_dir+"/wfg_api/output/"+user+"/download/"+date+"/"+e_folder+"/*/*/standard_report.json")[0]
    result_file = result_path+"/"+e_folder+".tsv"


    RESULT = open(result_file, "w")
    RESULT.write("\t".join(HEADER)+"\n")


    with open(file, "r") as f:
        json_dict = json.load(f)

        GENE_INFO = {}


        #Relations
        DRUG_INFO = {}
        RELATIONS = {
            "prognosis":[],
            "drug": ""
        }
        if json_dict.has_key("Relations"):
            buf1 = json_dict["Relations"]
            if buf1.has_key("Prognoses"):
                p_list = buf1["Prognoses"]
                for p in p_list:
                    RELATIONS["prognosis"].append(find_text("VariantId", p))

            if buf1.has_key("GeneVariantEvidenceLevels"):
                v_list = buf1["GeneVariantEvidenceLevels"]
                for v in v_list:
                    gene = v["VariantIds"][0]
                    if not DRUG_INFO.has_key(gene):
                        DRUG_INFO[gene] = {
                            "drug_name": [],
                            "evidence_level": [],
                            "evidence_text": [],
                            "drug_target": [],
                            #"fda_text": [],
                            "nctid": [],
                            "pmid": []
                        }

                    #PMIDs
                    PMID = []
                    text = str(find_text("Evidences", v))
                    pa = r"[0-9]{8}"
                    match = re.findall(pa, text)
                    PMID.extend(match)
                    
                    text = str(find_text("FdaApprovedConditions", v))
                    match = re.findall(pa, text)
                    PMID.extend(match)
                    
                    #drug
                    DRUG = find_text("DrugName", v)

                    #Evidence Text
                    ET = DRUG+"["
                    if v.has_key("Evidences"):
                        j = v["Evidences"][0]
                        if j.has_key("Summary"):
                            ET += "Summary: "+j["Summary"]+","
                        if j.has_key("Evidence"):
                            ET += "Evidence: "+j["Evidence"]
                    ET += "]"

                    DRUG_INFO[gene]["drug_name"].append(DRUG)
                    DRUG_INFO[gene]["evidence_level"].append(find_text("EvidenceLevel", v))
                    DRUG_INFO[gene]["evidence_text"].append(ET)
                    DRUG_INFO[gene]["drug_target"].append(find_text("DrugAssociations", v))
                    #DRUG_INFO[gene]["fda_text"].append(find_text("FdaApprovedConditions", v))
                    DRUG_INFO[gene]["nctid"].append(find_text("ClinicalTrials", v))
                    DRUG_INFO[gene]["pmid"].extend(PMID)

            RELATIONS["drug"] = DRUG_INFO
            #RELATIONS["pmid"] = PMID
        else:
            RELATIONS["drug"] = ""
            #RELATIONS["pmid"] = ""


        
        
        #sample info
        SAMPLE_INFO = {}
        if json_dict.has_key("SampleInfo"):
            buf = json_dict["SampleInfo"]
            SAMPLE_INFO["Age"] = buf["Age"]
            SAMPLE_INFO["Gender"] = buf["Gender"]
            SAMPLE_INFO["ConditionId"] = buf["ConditionId"]
            SAMPLE_INFO["ConditionName"] =  buf["ConditionName"]
            

        #gene
        if json_dict.has_key("Genes"):
            gene_list = json_dict["Genes"]

            for gl in gene_list:
                GN = find_text("GeneName", gl)
                GS = find_text("GeneSummary", gl)
                CS = find_text("Chromosome", gl)
                PT = find_text("PrimaryTranscript", gl)
                PS = find_text("Position", gl)
                HDEL = find_text("HighestDrugEvidenceLevel", gl)
                GA = find_text("GeneAnnotation", gl)

                
                VARIANT = {}
                for vas in find_text("Variants", gl):
                    VT = find_text("Variant", vas)
                    VID = find_text("VariantId", vas)
                    VTYPE = find_text("VariantType",vas)
                    CLC = find_text("ChromosomeLocationChange", vas)
                    AA = find_text("AminoAcid", vas)
                    DNAC = find_text("DNACoding", vas)
                    CF = find_text("Classification", vas)
                    CFS = find_text("ClassificationSource", vas)
                    EF = find_text("Effect", vas)
                    TI = find_text("TranscriptId", vas)
                    AF = find_text("AlleleFrequency", vas)
                    SD = find_text("SequencingDepth", vas)
                    
                    IV_LOG2 = ""
                    if vas.has_key("InputValue"):
                        if vas["InputValue"].has_key("Unit"):
                            unit = vas["InputValue"]["Unit"]
                            if unit == "log2":
                                IV_LOG2 = vas["InputValue"]["Value"]


                    AT = ""
                    if vas.has_key("AlterationSummary"):
                        if vas["AlterationSummary"].has_key("WfGAnnotations"):
                            vas2 = vas["AlterationSummary"]["WfGAnnotations"][0]
                            if vas2.has_key("AnnotationText"):
                                AT = vas2["AnnotationText"]

                    ODI = find_text("OtherDatabaseIds", vas)

                    MARK = []
                    if vas.has_key("PredisposingMutationInfo"):
                        MARK.append("Predisposing")

                    LOG2 = ""
                    if VID in RELATIONS["prognosis"]:
                        MARK.append("Prognosis")

                    #if IV_LOG2 == "":
                    if log2_dict.has_key(GN):
                        IV_LOG2 = str(log2_dict[GN][1])

                    if AF == "" or SD == "":
                        if vaf_dict.has_key(CS+"_"+PS):
                            AF = vaf_dict[CS+"_"+PS][0]
                            SD = vaf_dict[CS+"_"+PS][1]

                    if AF != "":
                        AF = "AF=" + AF
                    if SD != "":
                        SD = "DP=" + SD
                    if IV_LOG2 != "":
                        IV_LOG2 = "log2=" + str(IV_LOG2)

                    VARIANT[VT] = [VID,VTYPE,CLC,AA,DNAC,CF,CFS,EF,IV_LOG2,TI,AF,SD,AT,ODI]

                    GENE_INFO[GN] = [GS,CS,PT,PS,GA,VARIANT]

                    
                    DN, EL, ET, DT, FT, PMID, NI = "", "", "", "", "", "", ""
                    drug_hash = {
                        "1": [],
                        "2A": [],
                        "2B": [],
                        "3A": [],
                        "3B": [],
                        "4": []
                    }

                    if RELATIONS["drug"].has_key(VID):
                        buf = RELATIONS["drug"][VID]

                        DN = buf["drug_name"]
                        EL = buf["evidence_level"]
                        for i in range(len(EL)):
                            drug_hash[str(EL[i])].append(DN[i])


                        ET = "-------------------".join(buf["evidence_text"])
                        DT = buf["drug_target"]
                        #FT = buf["fda_text"]
                        arr = ("PMID:" + x for x in buf["pmid"])
                        PMID = ",".join(arr)

                        pa = "NCT[0-9]{8}"
                        nctid = re.findall(pa, str(buf["nctid"]))
                        NI = ",".join(nctid)



                    OUTPUT = [
                        e_folder,  #RIMS ID
                        SAMPLE_INFO["Age"],
                        SAMPLE_INFO["Gender"],
                        SAMPLE_INFO["ConditionName"],
                        CS,  #Chromesome
                        PS,  #Position
                        GN,  #GeneName
                        VID,  #Variant
                        VTYPE,  #vatiant type
                        CLC,  #chromosome location change
                        AA,  #Amino acid
                        DNAC,  #DNACoding
                        CF,  #Classification(vus)
                        ":".join(MARK),  #Prognosis
                        TI,  #Refference ID
                        CF,  #Classification
                        CFS,  #Classification source
                        EF,  #Effect
                        AF,  #Allele Freqency
                        SD,  #Sequencing Depth
                        IV_LOG2,  #log2
                        ",".join(drug_hash["1"]),
                        ",".join(drug_hash["2A"]),
                        ",".join(drug_hash["2B"]),
                        ",".join(drug_hash["3A"]),
                        ",".join(drug_hash["3B"]),
                        ",".join(drug_hash["4"]),
                        NI,  #NCTID
                        PMID,  #PMID
                        AT,  #annotation text
                        ET  #evidence text
                        #FT  #fda text
                    ]
                    RESULT.write("\t".join(OUTPUT)+"\n")

    RESULT.close()


form = cgi.FieldStorage()
e_folder = form.getvalue("folder", "0")
user = form.getvalue("user", "0")
serialno = form.getvalue("serialno", "0")

cur_dir = "/var/www/cgi-bin"
result_path = "/var/www/htdocs/output"
input_folder = cur_dir+"/wfg_api/input/"+serialno+"/"+e_folder


func(cur_dir,input_folder,result_path,user,serialno,e_folder)
print "Content-type: text/plain; charset='utf-8'\n"
print user+","+e_folder+","+serialno



sys.exit()

