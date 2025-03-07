# Splice_finder
* These scripts are inspired by SplicdFinder https://github.com/deepomicslab/SpliceFinder/tree/master.
* We provide two ways to detect splice doner and acceptor: 1. by exon position 2. by TF based model (models from SpliceFinder github)
# How to define Donor and Acceptor
 * protein coding genes
 * have more than 1 exons
 * first exon does not have acceptor and last exon does not have Donor
 * Reverse the seq if strand is "-"
  
## 1. Finding Splice doner and acceptor for single gene
*   1.1 run splice_motif_finder_single_gene_UCSC.sh in sh_files folder 
*   1.2 run Splice_motif_ggseqlogo.Rmd in R folder to get splice Doner and Acceptor motif logos
 
## 2. Finding Splice doner and acceptor for all protein-coding genes
   2.1 run splice_motif_finder_All_protein_coding_gene_UCSC.sh in sh_files folder 
   2.2 run Splice_motif_ggseqlogo.Rmd in R folder to get splice Doner and Acceptor motif logos


