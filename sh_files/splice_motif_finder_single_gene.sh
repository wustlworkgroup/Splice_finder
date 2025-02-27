#!/bin/bash

# This programe was inspired by spliceFinder: https://pubmed.ncbi.nlm.nih.gov/31881982/
# Initialize Mamba and activate the environment
# download Homo_sapiens.GRCh38.86.gtf.gz from https://ftp.ensembl.org/pub/release-86/gtf/homo_sapiens/; save to REF path
# download Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa https://ftp.ensembl.org/pub/release-86/fasta/homo_sapiens/dna/ save to REF path
# exon data is download from https://drive.google.com/drive/folders/1b8M-OgIyYyr__Rx0XS8uZAeHgFsMuHF_
# Deep-learning was provided in another script

  REF_path=/media/yang/Data/SliceFinder/Ref/Hg38 
  sh_files_path=/media/yang/Data/SliceFinder/sh_files
  Hg38_fa=$REF_path/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa
  GTF_file=$REF_path/Homo_sapiens.GRCh38.86.gtf.gz
  PY_function_path=/media/yang/Data/SliceFinder/PY_function
  Output_path=/media/yang/Data/SliceFinder/out_predict/BY_EXON
  mkdir -p $Output_path
  source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2
  gene_name=CDKN2A
  echo "$gene_name"
  bash ${sh_files_path}/splice_motif_finder_argu.sh $REF_path $PY_function_path $gene_name $Output_path  
  exit



