# Splice_finder
* These scripts are inspired by SplicdFinder https://github.com/deepomicslab/SpliceFinder/tree/master.
* We provide two ways to detect splice doner and acceptor: 1. by exon position 2. by TF based model (models from SpliceFinder github)
# How to define Donor and Acceptor
 * protein coding genes
 * have more than 1 exons
 * first exon does not have acceptor and last exon does not have Donor
 * Reverse the seq if strand is "-"
 * In our code, only choose the transcript with max number of exons if gene has mulitple transcripts 
  
## 1. Finding Splice doner and acceptor for single gene
*   1.1 run splice_motif_finder_single_gene_UCSC.sh in sh_files folder 
*   1.2 run Splice_motif_ggseqlogo.Rmd in R folder to get splice Doner and Acceptor motif logos
*   1.3 examples: NF1 strand +; CDKN2A strand -, MTAP strand +; 
 
## 2. Finding Splice doner and acceptor for all protein-coding genes
  * 2.1 run splice_motif_finder_All_protein_coding_gene_UCSC.sh in sh_files folder
  * 2.2 run Splice_motif_ggseqlogo_ALL_genes.Rmd in R folder to get splice Doner and Acceptor motif logos ( input donor and acceptor file)


