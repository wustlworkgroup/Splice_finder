#!/bin/bash

# This programe was inspired by spliceFinder: https://pubmed.ncbi.nlm.nih.gov/31881982/
# Initialize Mamba and activate the environment
# download Homo_sapiens.GRCh38.86.gtf.gz from https://ftp.ensembl.org/pub/release-86/gtf/homo_sapiens/; save to REF path
# download Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa https://ftp.ensembl.org/pub/release-86/fasta/homo_sapiens/dna/ save to REF path
# exon data is download from https://drive.google.com/drive/folders/1b8M-OgIyYyr__Rx0XS8uZAeHgFsMuHF_
# Deep-learning was provided in another script

  REF_path=/media/yang/Data/SliceFinder/Ref/Hg38 

  Hg38_fa=$REF_path/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa
  GTF_file=$REF_path/Homo_sapiens.GRCh38.86.gtf
  PY_function_path=/media/yang/Data/SliceFinder/PY_function
  gene_input=NF1
  Output_path=/media/yang/Data/SliceFinder/out_predict/${gene_input}
  mkdir -p $Output_path
  source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2
  
  # get gene exons and donor and acceptor information
  if [ ! -f "$Output_path/${gene_input}_exons.csv" ]; then
    echo "get exons from $gene_input and save it to $Output_path/${gene_input}_exons.csv"
    python3 $PY_function_path/Extract_Exons_From_Gene.py $GTF_file $gene_input $Output_path
  fi
  
  if [ ! -f $Output_path/${gene_input}_dna_acceptor_loc ]; then
   python3 $PY_function_path/generate_gene.py "$Output_path/${gene_input}_exons.csv" $REF_path $Output_path
  fi
  
  sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_donor_loc" > "$Output_path/${gene_input}_dna_donor_loc2"
  sh $Output_path/${gene_input}_dna_donor_loc2 > $Output_path/${gene_input}_dna_donor_seq

 sed "s|^|samtools faidx $Hg38_fa |" "$Output_path/${gene_input}_dna_acceptor_loc" > "$Output_path/${gene_input}_dna_acceptor_loc2"
  sh $Output_path/${gene_input}_dna_acceptor_loc2 > $Output_path/${gene_input}_dna_acceptor_seq

 exit
 # Gene loc annotation



