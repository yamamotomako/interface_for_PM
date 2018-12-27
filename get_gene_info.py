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


def get_gene_info(json_dict):

    GENE_INFO = {}

    if json_dict.has_key("Genes"):
        gene_list = json_dict["Genes"]

        for gl in gene_list:
            GN = find_text("GeneName", gl)
            # GS = find_text("GeneSummary", gl)
            # CS = find_text("Chromosome", gl)
            # PT = find_text("PrimaryTranscript", gl)
            # PS = find_text("Position", gl)
            GA = find_text("GeneAnnotation", gl)

            VARIANT = {}
            for vas in find_text("Variants", gl):
                # VT = find_text("Variant", vas)
                VID = find_text("VariantId", vas)
                # VTYPE = find_text("VariantType",vas)
                # CLC = find_text("ChromosomeLocationChange", vas)
                # AA = find_text("AminoAcid", vas)
                # DNAC = find_text("DNACoding", vas)
                # CF = find_text("Classification", vas)
                # CFS = find_text("ClassificationSource", vas)
                # EF = find_text("Effect", vas)
                # TI = find_text("TranscriptId", vas)
                # AF = find_text("AlleleFrequency", vas)
                # SD = find_text("SequencingDepth", vas)

                AT = ""
                if vas.has_key("AlterationSummary"):
                    if vas["AlterationSummary"].has_key("WfGAnnotations"):
                        vas2 = vas["AlterationSummary"]["WfGAnnotations"][0]
                        if vas2.has_key("AnnotationText"):
                            AT = vas2["AnnotationText"]

                # ODI = find_text("OtherDatabaseIds", vas)

                VARIANT[VID] = AT
                #VARIANT[VT] = [VID,VTYPE,CLC,AA,DNAC,CF,CFS,EF,TI,AF,SD,AT,ODI]

            GENE_INFO[GN] = [GA, VARIANT]
            #GENE_INFO[GN] = [GS,CS,PT,PS,GA,VARIANT]

        return GENE_INFO



#file_path = "./result/miseq.myeloid_panel.20180807/json/3_S3.json"
#file_path = "./result/"+form.getvalue("file_path",0)
file_path = "./result/"+sys.argv[1]

result = {}

def main():
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        result = get_gene_info(json_dict)

    return json.dumps(result)


print main()
