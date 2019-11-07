# here we import pandas (install via conda)
import pandas as pd

# load all sample we want to process
proteomes = pd.read_table("proteomes/proteome_names.txt")

proteintable = pd.read_table("proteins/protein_names.tab")

rule all:
	input:
		#"proteomes/Proteomes_combined.pdb"
		expand("groups/{protein_names}_blastgroups.fa",
			protein_names = proteintable.Entry)

rule combine_proteomes:
	input:
		expand("proteomes/{proteome_name}.fasta", proteome_name = proteomes.File)
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
		"proteomes/Proteomes_combined_map.pdb"
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
		wget -O {output} https://www.uniprot.org/uniprot/{wildcards.protein_name}.fasta 
		"""

rule blastp:
	input:
		query = "proteins/{protein_name}.fasta",
		database = "proteomes/Proteomes_combined.fasta"
	output:
		"hits/{protein_name}_blast.txt"
	shell:
		"""
		blastp -query {input.query} -db {input.database} -out {output} -outfmt "6 qacc sacc evalue "
		"""

rule seq_groups:
	input:
		blast = "hits/{protein_name}_blast.txt",
		proteome = "proteomes/Proteomes_combined.fasta"
	output:
		"groups/{protein_name}_blastgroups.fa"
	run:
		import pandas as pd
		from pyfaidx import Fasta

		blast = pd.read_csv(input.blast,sep="\t", header=None)
		prot  = Fasta(input.proteome)

		with open(output[0], "w") as fastaout:
			for index, row in blast.iterrows():
				seq = prot[row.loc[1]]
				fastaout.write(f">{row.loc[1]}\n{seq}\n")


rule alignments:
	input:
		"groups/{protein_name}_blastgroups.fa"
	output:
		"alignments/{protein_name}_blastgroups.aln"
	conda:
		"env/clustal.yml"
	shell:
		"""
		clustalo -i {input} --seqtype=Protein -o {output}
		"""
