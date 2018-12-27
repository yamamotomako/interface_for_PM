#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import json
import cgi
import glob


file_path = "./result/"+sys.argv[1]
drug = sys.argv[2]

def main():
    with open(file_path, "r") as f:
        lines = f.read()
        return lines


print main()
