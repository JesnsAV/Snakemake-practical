import pandas as pd

configfile: "config/config.yaml"

samples = pd.read_csv("config/samples.tsv", sep="\t")

rule all:
	input:
		expand("{results}/nuc_diversity.pdf",results=config["results"])

rule combine_proteomes:
	input:
		ref="{data}/TB_ref.fa",
		vcf="{data}/known_variants.vcf.gz"
	output:
		directory("{data}/gramtools/build")
	params:
		#?
	singularity:
		config["?"]
	shell:
		#?
