
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
