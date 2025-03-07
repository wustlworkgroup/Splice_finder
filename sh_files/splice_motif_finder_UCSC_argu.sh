# Parse command-line arguments
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <REF_path> <PY_function_path> <gene_input> <Output_path> <GTF_file> <hg38_fa> "
    exit 1
fi

REF_path=$1
PY_function_path=$2
gene_input=$3
Output_path1=$4
Output_path=${Output_path1}/${gene_input}

GTF_file=$5
Hg38_fa=$6
All_genes_exon="$REF_path/all_genes_UCSC_exons.csv"

mkdir -p "$Output_path"
source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2

if [ ! -f "$REF_path/UCSC_Ref_all_genes_exons.csv" ]; then
    python3 $PY_function_path/Extract_Exons_From_All_genes_ucsc.py $GTF_file $REF_path
fi


# Get gene exons and donor and acceptor information
if [ ! -f "$Output_path/${gene_input}_UCSC_exons.csv" ]; then
    echo "Extracting exons for $gene_input..."
    python3 "$PY_function_path/Extract_Exons_From_Gene_UCSC.py" "$REF_path/UCSC_Ref_all_genes_exons.csv" "$gene_input" "$Output_path" 
fi


if [ ! -f "$Output_path/${gene_input}_dna_acceptor_loc" ]; then
    echo "Generating gene location and splice information..."
    #python3 "$PY_function_path/generate_gene.py" "$Output_path/${gene_input}_exons.csv" "$REF_path" "$Output_path"
    python3 "$PY_function_path/generate_gene_by_exon_position_UCSC.py" "$Output_path/${gene_input}_exons.csv" "$REF_path" "$Output_path"
fi

# Check if the file is empty
if [[ -f "$Output_path/${gene_input}_dna_acceptor_loc" ||  -f "$Output_path/${gene_input}_neg_dna_acceptor_loc"  ]]; then
   echo "correct acceptor and donor loc"
 else 
  echo "Error: No data found in dna_acceptor_loc"
    exit 1
fi

# Extract sequences using samtools
if [ -f $Output_path/${gene_input}_dna_donor_loc ]; then
 echo "gene with strand pos"
 sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_donor_loc" > "$Output_path/${gene_input}_dna_donor_loc2"
 sh "$Output_path/${gene_input}_dna_donor_loc2" > "$Output_path/${gene_input}_dna_donor_seq"
 sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_acceptor_loc" > "$Output_path/${gene_input}_dna_acceptor_loc2"
 sh "$Output_path/${gene_input}_dna_acceptor_loc2" > "$Output_path/${gene_input}_dna_acceptor_seq"
fi

if [ -f $Output_path/${gene_input}_neg_dna_donor_loc ]; then 
 echo "gene with strand neg"
 sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_neg_dna_donor_loc" > "$Output_path/${gene_input}_dna_donor_loc2"
 sh "$Output_path/${gene_input}_dna_donor_loc2" > "$Output_path/${gene_input}_neg_dna_donor_seq"
 sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_neg_dna_acceptor_loc" > "$Output_path/${gene_input}_dna_acceptor_loc2"
 sh "$Output_path/${gene_input}_dna_acceptor_loc2" > "$Output_path/${gene_input}_neg_dna_acceptor_seq"

 # Reverse complement using Bash
 #awk 'NR % 2 == 1 {print; next} {print | "rev | tr \"ATCGatcg\" \"TAGCtagc\""}' "${Output_path}/${gene_input}_neg_dna_donor_seq" > "${Output_path}/${gene_input}_dna_donor_seq"

 awk '
    NR % 2 == 1 {print; next} 
    { 
        cmd = "echo " $0 " | rev | tr \"ATCGatcg\" \"TAGCtagc\""; 
        cmd | getline rev_seq; 
        close(cmd); 
        print rev_seq;
    }
' "${Output_path}/${gene_input}_neg_dna_donor_seq" > "${Output_path}/${gene_input}_dna_donor_seq"

  awk '
    NR % 2 == 1 {print; next} 
    { 
        cmd = "echo " $0 " | rev | tr \"ATCGatcg\" \"TAGCtagc\""; 
        cmd | getline rev_seq; 
        close(cmd); 
        print rev_seq;
    }
' "${Output_path}/${gene_input}_neg_dna_acceptor_seq" > "${Output_path}/${gene_input}_dna_acceptor_seq"


fi

exit 0
