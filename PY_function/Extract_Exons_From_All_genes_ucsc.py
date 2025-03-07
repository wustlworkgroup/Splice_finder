import argparse
import os
import pandas as pd
#from gtfparse import read_gtf

parser = argparse.ArgumentParser(description="Extract exons for a specific gene from a exons_list_file")
parser.add_argument("gtf_file", type=str, help="UCSC gtf file path")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()

gtf_file = args.gtf_file
# Read the GTF file
columns = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame","attributes"]
gtf_data = pd.read_csv(gtf_file, sep="\t", comment="#", names=columns, dtype=str,header=None)


# Function to extract gene_id and gene_name from attributes column
def extract_attributes(attribute_text):
    attributes = {}
    for item in attribute_text.split(";"):
        if item.strip():
            key_value = item.strip().split(" ", 1)
            if len(key_value) == 2:
                key, value = key_value
                attributes[key.strip()] = value.strip().strip('"')  # Remove surrounding quotes
    return attributes

attributes_df = gtf_data["attributes"].apply(extract_attributes).apply(pd.Series)
gtf_data = pd.concat([gtf_data.drop(columns=["attributes"]), attributes_df], axis=1)

filtered_gtf_data = gtf_data[gtf_data["gene_name"].notna() & (gtf_data["gene_name"] != "") & (gtf_data["feature"]=="exon" ) ]

output_file = os.path.join(args.Out_path, "UCSC_Ref_all_genes_exons.csv")
filtered_gtf_data.to_csv(output_file, index=False)

