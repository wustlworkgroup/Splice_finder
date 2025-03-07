#!/bin/bash
# For the UCSC data
# This programe was inspired by spliceFinder: https://pubmed.ncbi.nlm.nih.gov/31881982/
# Initialize Mamba and activate the environment
# download Hg38.fa from https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/; save to REF path
# download hg38.knowGene.gtf https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/ save to REF path
# OR ncbiRefSeq From https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/ncbiRefSeqCurated.txt.gz
# Deep-learning was provided in another script

  REF_path=/media/yang/Data/SliceFinder/Ref/Hg38_UCSC 
  sh_files_path=/media/yang/Data/SliceFinder/sh_files
  Hg38_fa=$REF_path/hg38.fa
  GTF_file=$REF_path/hg38.refGene.gtf
  All_genes_exons_file=$REF_path/UCSC_Ref_all_genes_exons.csv
  PY_function_path=/media/yang/Data/SliceFinder/PY_function
  Output_path=/media/yang/Data/SliceFinder/out_predict/All_genes
  mkdir -p $Output_path
  source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2

  start_time=$(date +"%Y-%m-%d %H:%M:%S")
  echo "Script started at: $start_time"

  if [ ! -f "$REF_path/All_protein_coding_gene_names.txt" ]; then
    python3 $PY_function_path/Extract_all_coding_genes_UCSC.py $All_genes_exons_file $REF_path
  fi
   
 

   # Create empty files to store combined sequences
  > "$Output_path/All_donor_seq"
  > "$Output_path/All_acceptor_seq"

 # Process only the first 10 rows of the gene list
   while IFS=$'\t' read -r gene_name; do
    echo "$gene_name"
    bash "${sh_files_path}/splice_motif_finder_UCSC_argu.sh" "$REF_path" "$PY_function_path" \
         "$gene_name" "$Output_path" "$GTF_file" "$Hg38_fa" 
  
    donor_file=$Output_path/$gene_name/${gene_name}_dna_donor_seq
    acceptor_fle=$Output_path/$gene_name/${gene_name}_dna_acceptor_seq
    cat $donor_file >> $Output_path/All_donor_seq
    cat $acceptor_fle >> $Output_path/All_acceptor_seq
    rm -r $Output_path/$gene_name
  done < "$REF_path/All_protein_coding_gene_names.txt" 

 end_time=$(date +"%Y-%m-%d %H:%M:%S")
 echo "Script completed at: $end_time"
 exit



