#main_step = 'orf_predict, filter, annotate, quantify, report'
main_step = 'assemble'
#main_step = 'readsqc, assemble, orf_predict, filter, quantify'

#global configs
threads = 1
processes = 1
logs_dir = 'logs'

#readsqc configs
kneaddata_exe = 'kneaddata'
kneaddata_path = ''         #default install with conda
trimmomatic_path = 'trimmomatic'

#assemble configs
megahit_exe = 'megahit'
megahit_path = ''
metaspades_exe = 'metaspades.py'
metaspades_path = ''
assembler = 'megahit'
memory = 100

#filter configs
reformat_exe = 'bbduk.sh'
reformat_path  = ''
cdhitest_exe = 'cd-hit-est'
cdhit_exe = 'cd-hit'
cdhit_path = ''
min_contig_length = 500
max_contig_length = 150000
min_contig_id = 0
min_contig_coverage = 0
min_protein_length = 100
max_protein_length = 150000
min_id = 0.95
min_coverage = 0


#orf predict configs
prodigal_exe = 'prodigal'
prodigal_path = ''

#annotate configs
blastp_exe = 'blastp'
blastx_exe = 'blastx'
blast_path = ''
diamond_exe = 'diamond'
diamond_path = ''
blast_type = 'blastp'

diamond_params = "--top 10 --outfmt 6 qseqid sseqid bitscore evalue pident length stitle"
blast_params = "-max_target_seqs 10 -outfmt '6 qseqid sseqid bitscore evalue pident length stitle staxid'"

#quantify configs
salmon_exe = 'salmon'
salmon_path = ''

#kraken2 options
kraken2_exe = 'kraken2'
kraken2_path = ''