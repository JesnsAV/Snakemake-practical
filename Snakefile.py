# here we import pandas (install via conda)
import pandas as pd

# load all sample we want to process
samples = pd.read_table("proteomes/proteome_names.txt")


rule all:
	input:
		"proteomes/Proteomes_combined.fasta"

rule combine_proteomes:
	input:
		expand("proteomes/{proteome_name}.fasta", proteome_name = samples.File)
	output:
		"proteomes/Proteomes_combined.fasta"
	shell:
		"""
		cat {proteome_name}.fasta > Proteomes_combined.fasta
		"""
