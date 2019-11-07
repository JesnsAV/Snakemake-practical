import pandas as pd

configfile: "config/config.yaml"

samples = pd.read_csv("config/samples.tsv", sep="\t")

rule all:
	input:
		proteomes/Proteomes_combined.fasta

rule combine_proteomes:
	input:
		proteomes/{proteome_name}.fasta
	output:
		proteomes/Proteomes_combined.fasta
	shell:
		"""
		echo {proteome_name}.fasta > Proteomes_combined.fasta
		"""
