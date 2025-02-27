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
chrom=df["Chromosome"][0]
gene=df["Gene"][0]


# find the splice site on the sequence
# Initialize splice site lists
left_splice = []
right_splice = []

# Iterate through each exon entry
for index, row in df.iterrows():
    if index != 0:
     left_splice.append(row["Start"])  # Get end position for left splice (acceptor)
    if index != len(df)-1:
     right_splice.append(row["End"])  # Get start position for right splice (donor)
    

# Convert lists to sets to get unique splice sites
left_splice = sorted(set(left_splice))
right_splice =sorted(set(right_splice))



print("splice site:")

         
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






