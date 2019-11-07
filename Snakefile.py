# here we import pandas (install via conda)
import pandas as pd

# load all sample we want to process
samples = pd.read_table("proteomes/proteome_names.txt")


rule all:
	input:
		"proteomes/Proteomes_combined.pdb"

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

def protein_names(wc):
	tbl = pd.read_table("resources/table")
	f = expand("proteins/{protfile}", protfile = tbl.entry)
	return(f)

rule retrieve_fastas:
	output:
		"proteins/{protein_name}.fasta"
	shell:
		"""
		wget ‐output-document={output} https://www.uniprot.org/uniprot/{wildcards.protein_name}.fasta
		"""
rule blastp:
	input:
		query = "proteins/{protein_name}.fasta"
		database = "proteomes/Proteomes_combined.fasta"
	output:
		"hits/{protein_name}_blast.txt"
	shell:
		"""
		blastp -query {input.query} -db {input.database} -out {output}
		"""
