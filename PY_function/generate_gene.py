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





# Save right_splice (donors) to donor file
donor_file = os.path.join(Out_path,f"{gene}_donor_sites.txt")

dna_donor_loc_file = os.path.join(Out_path, f"{gene}_dna_donor_loc")
with open(donor_file, 'w') as donor_out:
    donor_out.write("chrom\tposition\ttype\tfor_samtools\n")
    for pos in right_splice:
        donor_out.write(f"{chrom}\t{pos}\tdonor\t{chrom}:{pos-8}-{pos+4}\n")

with open(dna_donor_loc_file, 'w') as output:
    for pos in right_splice:
        a = chrom
        b = pos - 8
        c = pos + 4
        output.write(f"{a}:{b}-{c}\n")

# Save left_splice (acceptors) to donor file
acceptor_file = os.path.join(Out_path,f"{gene}_acceptor_sites.txt")
dna_acceptor_loc_file = os.path.join(Out_path, f"{gene}_dna_acceptor_loc")

with open(acceptor_file, 'w') as acceptor_out:
    acceptor_out.write("chrom\tposition\ttype\tfor_samtools\n")
    for pos in left_splice:
        acceptor_out.write(f"{chrom}\t{pos}\tacceptor\t{chrom}:{pos-20}-{pos+4}\n")

with open(dna_acceptor_loc_file, 'w') as output:
    for pos in left_splice:
        a = chrom
        b = pos - 20
        c = pos + 4
        output.write(f"{a}:{b}-{c}\n")


print(f"Saved donor sites to {donor_file}")
print(f"Saved acceptor sites to {acceptor_file}")






