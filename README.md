# Splice_finder
* These scripts are inspired by SplicdFinder https://github.com/deepomicslab/SpliceFinder/tree/master.
* We provide two ways to detect splice doner and acceptor: 1. by exon position 2. by TF based model (models from SpliceFinder github)
## 1. Finding Splice doner and acceptor  based on exon position (use gene name as input)
*   1.1 run splice_motif_finder.sh in sh_files folder 
*   1.2 run Splice_motif.Rmd in R folder to get splice Doner and Acceptor motif data matrix and plot logos

## 2. Find Splice doner and acceptor for mulitple genes (up to all protein-coding genes) 
*   1.1 run splice_all_coding_genes_motif_finder.sh in sh_files folder (get donor and acceptor sequence for genes)
*   1.2 run Splice_motif_multigenes.Rmd in R folder to get donor and acceptor data matrix and logos for multiple genes. 
      
## 3. Finding Splice doner and acceptor  based on TF model (use gene name as input, need more data for validation)
   2.1 run splice_motif_tf_predict.sh in sh_files folder
   2.2


