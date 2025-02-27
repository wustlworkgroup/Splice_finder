
# Parse command-line arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <REF_path> <PY_function_path> <gene_input> <Output_path>"
    exit 1
fi

REF_path=$1
PY_function_path=$2
gene_input=$3
Output_path1=$4
Output_path=${Output_path1}/${gene_input}
Hg38_fa="$REF_path/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa"
GTF_file="$REF_path/Homo_sapiens.GRCh38.86.gtf"
All_genes_exon="$REF_path/all_genes_exons.csv"

mkdir -p "$Output_path"
source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2

if [ ! -f $REF_path/all_genes_exons.csv ]; then
    python3 $PY_function_path/Extract_Exons_From_All_genes.py $GTF_file $REF_path
fi

# Get gene exons and donor and acceptor information
if [ ! -f "$Output_path/${gene_input}_exons.csv" ]; then
    echo "Extracting exons for $gene_input..."
   # python3 "$PY_function_path/Extract_Exons_From_Gene_2.py" "$GTF_file" "$gene_input" "$Output_path" 
   python3 "$PY_function_path/Extract_Exons_From_Gene_3.py" "$All_genes_exon" "$gene_input" "$Output_path" 
fi


if [ ! -f "$Output_path/${gene_input}_dna_acceptor_loc" ]; then
    echo "Generating gene location and splice information..."
    #python3 "$PY_function_path/generate_gene.py" "$Output_path/${gene_input}_exons.csv" "$REF_path" "$Output_path"
    python3 "$PY_function_path/generate_gene_by_exon_position.py" "$Output_path/${gene_input}_exons.csv" "$REF_path" "$Output_path"
fi

# Check if the file is empty
if [ ! -s "$Output_path/${gene_input}_dna_acceptor_loc" ]; then
    echo "Error: No data found in $Output_path/${gene_input}_dna_acceptor_loc"
    exit 1
fi



# Extract sequences using samtools
sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_donor_loc" > "$Output_path/${gene_input}_dna_donor_loc2"
sh "$Output_path/${gene_input}_dna_donor_loc2" > "$Output_path/${gene_input}_dna_donor_seq"

sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_acceptor_loc" > "$Output_path/${gene_input}_dna_acceptor_loc2"
sh "$Output_path/${gene_input}_dna_acceptor_loc2" > "$Output_path/${gene_input}_dna_acceptor_seq"

exit 0
