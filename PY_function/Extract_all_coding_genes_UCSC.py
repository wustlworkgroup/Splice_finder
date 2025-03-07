import argparse
import os
import pandas as pd
parser = argparse.ArgumentParser(description="Extract exons for a specific gene from a exons_list_file")
parser.add_argument("all_gene_exons_file", type=str, help="gene exons file path")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()

all_gene_exons=args.all_gene_exons_file

df = pd.read_csv(all_gene_exons, sep=",",header=0)

# Filter transcripts that contain "NM_" in the "transcript_id" column
df_filtered = df[df["transcript_id"].str.contains(r"NM_", na=False, regex=True)]
gene_names=set(df_filtered["gene_name"])

df_filtered = df[df["gene_name"].isin(gene_names)]
print(len(gene_names))

output_file = os.path.join(args.Out_path, "UCSC_protein_coding_gene.csv")
df_filtered.to_csv(output_file, index=False)

# Save unique gene names to a text file (19440)
gene_name_file=os.path.join(args.Out_path, "All_protein_coding_gene_names.txt")
with open(gene_name_file, "w") as f:
    for gene in gene_names:
        f.write(gene + "\n")

print("Gene names saved to All_protein_coding_gene_names.txt")



