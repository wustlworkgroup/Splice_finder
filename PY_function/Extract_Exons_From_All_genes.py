import argparse
import os
import pandas as pd
parser = argparse.ArgumentParser(description="Extract exons for a specific gene from a GTF file.")
parser.add_argument("gtf_file", type=str, help="Path to the input GTF file")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()
# Define column names based on GTF format
column_names = ["Chromosome", "Source", "Feature", "Start", "End", "Score", "Strand", "Frame", "Attributes"]

# Read the GTF file into a DataFrame
gtf_file = args.gtf_file
output_file = os.path.join(args.Out_path, "all_genes_exons.csv")


df = pd.read_csv(gtf_file, sep="\t", comment="#", names=column_names, header=None)

def extract_gene_name(attributes):
    for attr in attributes.split(";"):
        attr = attr.strip()
        if attr.startswith("gene_name"):
            return attr.split('"')[1]  # Extract value inside double quotes
    return None

def extract_transcript_id(attributes):
    for attr in attributes.split(";"):
        attr = attr.strip()
        if attr.startswith("transcript_id"):
            return attr.split('"')[1]  # Extract value inside double quotes
    return None

def extract_flag(attributes, flag_name):
    for attr in attributes.split(";"):
        attr = attr.strip()
        if attr.startswith(flag_name):
            value = attr.split('"')[1]  # Extract value inside quotes
            return value if value.strip() else "NA"  # Ensure empty values are replaced with "NA"
    return "NA"  # If the flag is missing, return "NA"

# Apply function to separate Transcript_ID and Tag correctly
#df_unique[["Transcript_ID", "Tag"]] = df_unique.apply(
#    lambda row: pair_transcript_tag(row["Transcript_ID"], row["Tag"]), axis=1, result_type="expand"
#)

df["Gene"]=df["Attributes"].apply(extract_gene_name)
df["Transcript_ID"]=df["Attributes"].apply(extract_transcript_id)
df["Tag"] = df["Attributes"].apply(lambda x: extract_flag(x, "tag"))


# Group by exon coordinates and gene, aggregating transcript IDs and tags separately
df_exons= df[df["Feature"] == "exon"].copy()
df_unique = (
    df_exons.groupby(["Chromosome", "Start", "End", "Gene"])  # Preserve NaN values
    .agg({
        "Transcript_ID": lambda x: ",".join(x.astype(str)),  # Keep NaN as string and maintain original order
        "Tag": lambda x: ",".join(x.astype(str))  # Keep NaN as string and maintain original order
    })
    .reset_index()
)





# Extract only exon entries

#df_unique = (
#    df_exons.groupby(["Chromosome", "Start", "End", "Gene"])
#    .agg({
#        "Transcript_ID": lambda x: ",".join(
#            sorted(
#                set(f"{tid}|{tag}" for tid, tag in zip(x, df_exons.loc[x.index, "Tag"])
#                    if pd.notna(tid) and pd.notna(tag))
#            )
#        ) if not x.isna().all() else "NA|NA"
#    })
#    .reset_index()
#)
df_unique.to_csv(output_file, index=False)

 


 
    
 
