import random
import linecache
import argparse
import numpy as np
import os
import pandas as pd

# choose gene splice area (left-1000,right+1000)
# 0 acceptor 1 donor 2 no splice
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Select gene splice area and generate labels.")
parser.add_argument("gene_exons_file", type=str, help="gene exons file path")
parser.add_argument("REF_path", type=str, help="Reference path for chromosome data")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()

REF_path = args.REF_path
gene_exons_file = args.gene_exons_file
Out_path = args.Out_path
REF_path =args.REF_path

df = pd.read_csv(gene_exons_file)
sorted_exons = df.sort_values(by=["Start"])
first_exon_start = sorted_exons.iloc[0]["Start"]
last_exon_end = sorted_exons.iloc[-1]["End"]
chrom=df["Chromosome"][0]
gene=df["Gene"][0]


print(gene)
#gene = linecache.getline(r'gene_loc_file', gene_num )
#chrom = gene.split('\t')[0]
start = int(first_exon_start) - 1000
stop = int(last_exon_end) + 1000
length = stop -start + 1
sample_num = length - 399


print("chromosome is %s"%chrom)
print("from %s"%start)
print("to %s"%stop)

# find the splice site on the sequence
left_splice = []
right_splice = []

exon_address = os.path.join(REF_path, f'chromosome/{chrom}/exon_uniq')
left_address = os.path.join(REF_path, f'chromosome/{chrom}/left_uniq')
right_address = os.path.join(REF_path, f'chromosome/{chrom}/right_uniq')


print("splice site:")
with open (exon_address) as input:
    for line in input:
        if int(line) >= start and int(line) <=stop:
            print(line)
            left = open(left_address,'r')
            right = open(right_address,'r')
            for left_loc in left:
                if int(left_loc)==int(line):
                    print('left')
                    if(int(line) not in left_splice):
                        left_splice.append(int(line))
                    break
            for right_loc in right:
                if int(right_loc)==int(line):
                    print('right')
                    if(int(line) not in right_splice):
                        right_splice.append(int(line))
            left.close()
            right.close()

print("Left (donor) splice sites:", left_splice)
print("Right (acceptor) splice sites:", right_splice)



# generate locations (For tensorflow)

out_file=os.path.join(Out_path,f"{gene}_dna_tf_loc")

with open (out_file,'w') as output:
    for i in range(start,start+sample_num):
        a=chrom
        b=i
        c=i+399
        output.write(str(a)+":"+str(b)+"-"+str(c)+"\n")


# generate labels

label=[]
label2=[]



tran_left=np.array(np.loadtxt(os.path.join(REF_path,'transcript_left')))
tran_right=np.array(np.loadtxt(os.path.join(REF_path,'transcript_right')))



for i in range(sample_num):
    label.append(2)
    label2.append(2)

for splice in left_splice:
    x = splice-start-200
    if (splice not in tran_left):
        label2[x]=0


for splice in right_splice:
    x = splice-start-199
    if (splice not in tran_right):
        label2[x]=1



label_file = os.path.join(Out_path, 'y_label')
label2_file = open(label_file,'w')
for i in range(sample_num):
    label2_file.write(str(label2[i]))
    label2_file.write('\t')

label2_file.close()

