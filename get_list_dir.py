#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
import json
import cgi
import glob
import re

#form = cgi.FieldStorage()

def func():
    result_str = ""

    for f in glob.glob("./result/*"):
        pattern = r"./result/(.+)$"
        match = re.search(pattern, f)
        folder = match.group(1)

        with open(f+"/config.tsv", "r") as f:
           lines = f.read().rstrip("\n").split("\n")
           for line in lines:
                if line[:11] == "folder_name":
                    continue
                data = line.split("\t")
                id = data[0].rstrip(" ")
                tmp = glob.glob("./result/"+folder+"/download/"+id+"/*")
                caseid =  os.path.basename(tmp[0])
                result_str += folder+"\t"+line+"\t"+caseid+"|||"


    return result_str.rstrip("\n")


print func()
#if __name__ == "__main__":
#    func()

#print "Content-type: text/plain; charset='utf-8'\n\n"
#print "Content-type: application/json; charset='utf-8'\n\n"
#print result_str.rstrip("\n")

