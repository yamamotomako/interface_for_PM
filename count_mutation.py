#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image, ImageDraw, ImageFilter

np.set_printoptions(threshold=np.inf)

GENE = []
GENE_freq = {}
GENE_hist = []

SAMPLE = []
SAMPLE_freq = {}
SAMPLE_hist = []

obj = {}


path = "./tsv"
for file in os.listdir(path):
    with open(path+"/"+file, "r") as f:
        lines = f.read().split("\n")
        file = file.replace(".tsv","")
        obj[file] = []

        for line in lines:
            data = line.split("\t")
            if data[0] == "sample":
                continue
            if data[0] == "":
                continue

            gene = data[3]

            if not gene in GENE_freq:
                GENE_freq[gene] = 1
            else:
                GENE_freq[gene] += 1

            if not file in SAMPLE_freq:
                SAMPLE_freq[file] = 1
            else:
                SAMPLE_freq[file] += 1

            obj[file].append(gene)


GENE_freq = sorted(GENE_freq.items(), key=lambda x: x[1], reverse=True)
SAMPLE_freq = sorted(SAMPLE_freq.items(), key=lambda x: x[1], reverse=True)

top_count = 0
for gene in GENE_freq:
    if top_count < 20:
    #if int(gene[1]) >= 10:
        GENE.append(gene[0])
        GENE_hist.append(gene[1])
        top_count += 1

for file in SAMPLE_freq:
    if not file in SAMPLE:
        SAMPLE.append(file[0])
        SAMPLE_hist.append(file[1])

RESULT = np.zeros((len(GENE), len(SAMPLE)))


for file in obj:
    for gene in obj[file]:
        if not gene in GENE:
            continue
        gene_index = GENE.index(gene)
        file_index = SAMPLE.index(file)
        RESULT[gene_index, file_index] = 1


df = pd.DataFrame(GENE_hist, index=GENE, columns=["count"])
fig = plt.figure(figsize=(3,8))
ax = fig.add_subplot(111)
sns.barplot(x="count", y=GENE, data=df, color="#08306b")
plt.tick_params(labelsize=5,labelbottom=False,labelleft=False,labelright=False,labeltop=False,color="w")
ax.spines["top"].set_linewidth(0)
ax.spines["bottom"].set_linewidth(0)
ax.spines["left"].set_linewidth(0)
ax.spines["right"].set_linewidth(0)
ax.set_xlabel("")
ax.set_ylabel("")
fig.patch.set_alpha(0)
plt.savefig("./gene_barplot.png")
#plt.show()
plt.close()


df = pd.DataFrame(SAMPLE_hist, index=SAMPLE, columns=["count"])
fig = plt.figure(figsize=(8,3))
ax = fig.add_subplot(111)
sns.barplot(x=SAMPLE, y="count", data=df, color="#08306b")
plt.tick_params(labelsize=5,labelbottom=False,labelleft=False,labelright=False,labeltop=False,color="w")
ax.spines["top"].set_linewidth(0)
ax.spines["bottom"].set_linewidth(0)
ax.spines["left"].set_linewidth(0)
ax.spines["right"].set_linewidth(0)
ax.set_xlabel("")
ax.set_ylabel("")
plt.savefig("./sample_barplot.png")
#plt.show()
plt.close()


df = pd.DataFrame(RESULT, index=GENE, columns=SAMPLE)
plt.figure(figsize=(8,8), dpi=180)
plt.axes([0.3,0.3,0.5,0.5])
plt.tick_params(labelsize=6)
sns.heatmap(df, cmap="Blues", cbar=False)
plt.savefig("./heatmap.png")
#plt.show()
plt.close()


img1 = Image.open("./gene_barplot.png")
img2 = Image.open("./heatmap.png")

back_im = img1.copy()
back_im.paste(img2, (100,50))
back_im.save("./all_heatmap.png", quality=95)





sys.exit()


#fig, ax = plt.subplots()
#ax.spy(RESULT, precision=0.1, markersize=5)
#ax.set_yticklabels(GENE)
#plt.show()






g_GENE = {}
path = "/home/ymako/for_kyoto/data_11"
for folder in os.listdir(path):
    try:
        os.path.exist(path+"/"+folder+"/"+folder+".genomon_mutation.result.txt")

    except:
        folder_rev = folder.replace("-","_")

    with open(path+"/"+folder+"/"+folder_rev+".genomon_mutation.result.txt", "r") as f:

        lines = f.read().split("\n")
        for line in lines:
            if line == "":
                continue
            if line[0] == "#":
                continue
            data = line.split("\t")
            if data[0] == "Chr":
                continue
            if data[0] == "":
                continue
            if data[5] != "exonic":
                continue

            func = data[5]
            print gene
            if data[6].find(",") != -1:
                gene = data[6].split(",")[0]
                gene_detail = data[6].split(",")[1]
            else:
                gene = data[6]
            dp = data[50]

            if not gene in g_GENE:
                g_GENE[gene] = 1
            else:
                g_GENE[gene] += 1

print g_GENE
