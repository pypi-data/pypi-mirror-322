import click
#from configs import config
import click_option_group
import decimal
from click_option_group import optgroup, OptionGroup, RequiredMutuallyExclusiveOptionGroup,RequiredAnyOptionGroup
from . import config

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

def add_options_test(options):
    def _add_options_test(func):
        print(options.get_options(''))
        for key in options.get_options('').keys():
            func = options.get_options('')[key]
        return func
    return _add_options_test
#def get_

#global options
global_options = OptionGroup('\nReadsqc model unique options')
global_options_list = [
    global_options.option(
        '-t', '--threads',
        type=int,
        default=config.threads,
        metavar='<int>',
        help = 'Number of threads. [default: '+str(config.threads)+ ']'
    ),
    global_options.option(
        '-p', '--processes',
        type=int,
        default=config.processes,
        metavar='<int>',
        help = 'number of processes. [default: '+str(config.processes)+ ']'
    ),
    global_options.option(
        '-m', '--memory',
        type=int,
        default = config.memory,
        metavar = '<int>',
        help = 'Memory limit in GB. [default: '+ str(config.memory) + ']'
    ),
    global_options.option(
        '-o', '--output',
        'output_dir',
        metavar = '<dirname>',
        help="Results will be saved in. Models' results will be saved in output/model.\n For example, results of readsqc will be in output/readsqc"
    ),
    global_options.option(
        '-l', '--logs',
        'logs_dir',
        metavar='<dirname>',
        help='Logs file will be stored in. Default: output/logs'
    )
]


#main options (whole model)
main_options_list = [
    click.option(
        '--step',
        default=config.main_step,
        help = 'Comma-separated list of steps to perform. [default: '+config.main_step + ']'
    )
]

main_input_options = RequiredAnyOptionGroup('\nMain Input')
main_input_list = [
    main_input_options.option(
        '-i','--input',
        metavar = '<filename>',
        default=[],
        multiple=True,
        help='Input FASTQ file'
    ),
    main_input_options.option(
        '--input-contigs',
        'input_contigs',
        metavar = '<filename>',
        help='Input Assembled contigs file'
    )
]

#readsqc model unique options
readsqc_options = OptionGroup('\nReadsqc model options')
readsqc_options_list = [
    #readsqc_config = OptionGroup('\nReadsqc model unique options', help='Test'),
    readsqc_options.option(
        '--bypass-trim',
        is_flag=True,
        help='Bypass the trim step'
    ),
    readsqc_options.option(
        '--host',
        default=[],
        multiple=True,
        metavar = '<filename>',
        help='Host genome database'
    )
]

readsqc_input_list = [
    click.option(
        '-i','--input',
        metavar = '<filename>',
        default=[],
        multiple=True,
        help='Input FASTQ file'
    )
]

#assemble model unique options
assemble_options = OptionGroup(name='\nAssemble model options')
assemble_options_list = [
    assemble_options.option(
        '-a','--assembler',
        type=click.Choice(['metaspades','megahit']),
        default=config.assembler,
        help='Assembly method. [default: '+ config.assembler + ']'
    )
]

assemble_input_options = OptionGroup(name='\nAssemble model input options')
assemble_input_list = [
    assemble_input_options.option(
        '-i1','--input1',
        metavar = '<filename>',
        help='Input FASTQ file'
    ),
    assemble_input_options.option(
        '-i2','--input2',
        metavar = '<filename>',
        help='Input FASTQ file'
    )
]



contig_filter_options = OptionGroup(name='\nContigs filter options')
contig_filter_list = [
    contig_filter_options.option(
        '--not-contig-filter',
        is_flag=True,
        help='Do not filter assembled contigs'
    ),
    contig_filter_options.option(
        '--min-contig-len',
        type=int,
        default=config.min_contig_length,
        metavar='<int>',
        help='Minimum contig size. [default: '+str(config.min_contig_length)+ ']'
    ),
    contig_filter_options.option(
        '--max-contig-len',
        type=int,
        default=config.max_contig_length,
        metavar='<int>',
        help='Maximum contig size. [default: '+str(config.max_contig_length)+ ']'
    ),
    contig_filter_options.option(
        '--min-contig-id',
        type=float,
        default=config.min_contig_id,
        metavar='<float>',
        help='Minimum contig identity. [default: '+str(config.min_id)+ ']'
    ),
    contig_filter_options.option(
        '--min-contig-coverage',
        type=float,
        default=config.min_contig_coverage,
        metavar='<float>',
        help='Minimum contig coverage. [default: '+str(config.min_coverage)+ ']'
    )
]

#filter model unique options
filter_options = OptionGroup(name='\nFilter options')
filter_options_list = [
    filter_options.option(
        '--seq-type',
        type=click.Choice(['prot','nucl']),
        default='prot',
        help='Molecule type of sequences. If provide two file, then one file will be filtered according to another.'
    ),
    filter_options.option(
        '--min-len',
        type=int,
        default=config.min_protein_length,
        metavar='<int>',
        help='Minimum fasta size. [default: '+str(config.min_protein_length)+ ']'
    ),
    filter_options.option(
        '--max-len',
        type=int,
        default=config.max_protein_length,
        metavar='<int>',
        help='Maximum fasta size. [default: '+str(config.max_protein_length)+ ']'
    ),
    filter_options.option(
        '--min-id',
        type=float,
        default=config.min_id,
        metavar='<float>',
        help='Minimum identity. [default: '+str(config.min_id)+ ']'
    ),
    filter_options.option(
        '--min-coverage',
        type=float,
        default=config.min_coverage,
        metavar='<float>',
        help='Minimum coverage. [default: '+str(config.min_coverage)+ ']'
    )
]

#input raw gene set
filter_input_options = OptionGroup(name='\nFilter Input Options')
filter_input_list = [
    filter_input_options.option(
        '-a', '--prot',
        metavar = '<filename>',
        help='Protein file need to be filtered'
    ),
    filter_input_options.option(
        '-d', '--nucl',
        metavar = '<filename>',
        help='Nucleotide file need to be filtered'
    )
]

#Orf Predict model unique options
orf_predict_input_list = [
    click.option(
        '--input-contigs',
        'contigs',
        metavar = '<filename>',
        help='Assembled contigs file'
    )
]

#annotate model unique options
annotate_options = OptionGroup(name='\nAnnotate model options')
annotate_options_list = [
    annotate_options.option(
        '--virus',
        metavar='<filename>',
        help='Virus database'
    ),
    annotate_options.option(
        '--non-virus',
        metavar='<filename>',
        help='Non-virus database'
    ),
    annotate_options.option(
        '-b', '--blast-type',
        type=click.Choice(['blastx','blastp']),
        default=config.blast_type,
        help='Assembly method. [default: '+ config.blast_type + ']'
    ),
    annotate_options.option(
        '-d', '--diamond',
        is_flag=True,
        help='Use Diamond to accelerate Blast'
    )
]

annotate_input_list = [
    click.option(
        '-q', '--query',
        required = True,
        metavar = '<filename>',
        help='File need to be annotated'
    )
]

#quantify model unique options
quantify_options = OptionGroup(name='\nQuantify model options')
quantify_options_list = [
    quantify_options.option(
        '--ref',
        'reference',
        required = True,
        metavar = '<filename>',
        help='Quantify Reference gene set'
    )
]

quantify_input_options = OptionGroup(name='\nQuantify model input options')
quantify_input_list = [
    quantify_input_options.option(
        '-i1','--input1',
        metavar = '<filename>',
        help='Input FASTQ file'
    ),
    quantify_input_options.option(
        '-i2','--input2',
        metavar = '<filename>',
        help='Input FASTQ file'
    )
]

#generate report model unique options
report_options = OptionGroup(name='\nClassification and Generate report model options')
report_options_list = [
    report_options.option(
        '--virus-anno',
        required = True,
        metavar = '<filename>',
        help='Blast/Diamond virus annotation file'
    ),
    report_options.option(
        '--nonvirus-anno',
        required = True,
        metavar = '<filename>',
        help='Blast/Diamond nonvirus annotation file'
    ),
    report_options.option(
        '--orf',
        required = True,
        metavar = '<filename>',
        help='Orf predict protein file'
    ),
    report_options.option(
        '--contigs',
        required = True,
        metavar = '<filename>',
        help='assembled contig file'
    ),
    report_options.option(
        '--quant',
        metavar = '<filename>',
        help='Quant file'
    )
]

#CAT options
CAT_options = OptionGroup(name='\nCAT options')
CAT_options_list = [
    CAT_options.option(
        '-r', '--ratio',
        default = decimal.Decimal('10'),
        type = decimal.Decimal,
        metavar = '<float>',
        help = r"CAT algorithm's r value. Only save %r scores"
    ),
    CAT_options.option(
        '--cluster-rep',
        is_flag=True,
        help='Use Cluster representive'
    ),
    CAT_options.option(
        '--cluster-file',
        metavar = '<filename>',
        help = 'Cluster file'
    )
]

 