#!/bin/bash

# Colocating indels and nucleotide differences
zcat <Ref2Ref>/quast_results/latest/contigs_reports/nucmer_output/*.used_snps.gz | awk '{print $1"\t"$3}' | uniq > snp1.txt
zcat <Assembly2Ref>/quast_results/latest/contigs_reports/nucmer_output/*.used_snps.gz | awk '{print $1"\t"$3}' | uniq > snp2.txt
cat snp1.txt snp2.txt > snps.txt
sort snps.txt | uniq -c | awk '{if ($1==2) print $0}' | awk '{if ($4=="."|| $5==".") print $0}' | wc -l # Count of shared indels
sort snps.txt | uniq -c | awk '{if ($1==2) print $0}' | awk '{if ($4!="."&&$5!=".") print $0}' | wc -l # Count of shared nucleotide differences
