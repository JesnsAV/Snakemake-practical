# here we import pandas (install via conda)
import pandas as pd

# load all sample we want to process
samples = pd.read_table("proteomes/proteome_names.txt")


rule all:
	input:
		"proteomes/Proteomes_combined_map.pdb"

rule combine_proteomes:
	input:
		expand("proteomes/{proteome_name}.fasta", proteome_name = samples.File)
	output:
		"proteomes/Proteomes_combined.fasta"
	shell:
		"""
		cat {input} > {output}
		"""
		
rule create_blastdb:
	input:
		"proteomes/Proteomes_combined.fasta"
	output:
		"proteomes/Proteomes_combined.pdb"
	shell:
		"""
		makeblastdb -in {input} -parse_seqids -blastdb_version 5 -title "Tgondii proteomes" -dbtype prot
		"""
