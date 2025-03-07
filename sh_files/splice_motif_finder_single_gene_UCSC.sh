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
  PY_function_path=/media/yang/Data/SliceFinder/PY_function
  Output_path=/media/yang/Data/SliceFinder/out_predict/BY_EXON
  mkdir -p $Output_path
  source /home/yang/anaconda3/bin/activate /home/yang/miniforge3/envs/keras2.2
  gene_name=CDKN2A
  echo "$gene_name"
  bash ${sh_files_path}/splice_motif_finder_UCSC_argu.sh $REF_path $PY_function_path \
          $gene_name $Output_path $GTF_file $Hg38_fa
  exit



