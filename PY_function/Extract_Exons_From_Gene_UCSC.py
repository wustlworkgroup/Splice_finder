import argparse
import os
import pandas as pd
parser = argparse.ArgumentParser(description="Extract exons for a specific gene from a exons_list_file")
parser.add_argument("all_gene_exons_file", type=str, help="gene exons file path")
parser.add_argument("gene_name", type=str, help="gene name input")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()

all_gene_exons=args.all_gene_exons_file
Gene_name=args.gene_name
df = pd.read_csv(all_gene_exons, sep=",",header=0)

df_genes = df[df["gene_name"] == Gene_name ].copy()

print(df_genes.head())

output_file = os.path.join(args.Out_path, f"{args.gene_name}_exons.csv")
df_genes.to_csv(output_file, index=False)
