import argparse
import os
import pandas as pd

def read_gtf(gtf_file, gene_name):
    """Reads a GTF file and extracts exon start and end sites for a specific gene."""
    exons = []
    left_splice = []  # Acceptor sites
    right_splice = []  # Donor sites

    with open(gtf_file, 'r') as file:
        for line in file:
            if line.startswith("#"):  # Skip header lines
                continue

            fields = line.strip().split('\t')
            if len(fields) < 9 or fields[2] != "exon":  # Ensure valid exon entry
                continue

            chrom = fields[0]
            start = int(fields[3])
            end = int(fields[4])
            gene_info = fields[8]

            # Extract gene name from attributes
            attributes = gene_info.split(';')
            extracted_gene_name = None
            for attr in attributes:
                if "gene_name" in attr:
                    extracted_gene_name = attr.split('"')[1]
                    break  # Stop once the gene name is found

            if extracted_gene_name == gene_name:
                exons.append([chrom, start, end, extracted_gene_name])
                left_splice.append(start)  # Acceptor site
                right_splice.append(end)  # Donor site

    return exons, left_splice, right_splice

def main():
    parser = argparse.ArgumentParser(description="Extract exons for a specific gene from a GTF file.")
    parser.add_argument("gtf_file", type=str, help="Path to the input GTF file")
    parser.add_argument("gene_name", type=str, help="Gene name to extract exon data for")
    parser.add_argument("Out_path", type=str, help="Output directory for generated files")
    args = parser.parse_args()

    exons, left_splice, right_splice = read_gtf(args.gtf_file, args.gene_name)

    if exons:
        print(f"Extracted exons for gene: {args.gene_name}")
        df = pd.DataFrame(exons, columns=["Chromosome", "Start", "End", "Gene"])
        output_file = os.path.join(args.Out_path, f"{args.gene_name}_exons.csv")
        df.to_csv(output_file, index=False)
        print(f"Exon coordinates saved to {output_file}")
    else:
        print(f"No exons found for gene {args.gene_name} in {args.gtf_file}.")

if __name__ == "__main__":
    main()

