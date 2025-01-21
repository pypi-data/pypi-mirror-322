import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )
import numpy as np
import pandas as pd
import subprocess
import traceback
import argparse
from .find_options import find_advanced_options
import utilities
import click
from click_option_group import optgroup
#from ..configs.global_args import GlobalArgs
from configs import options
from configs import config

import logging

logger=logging.getLogger(__name__)

@click.command(
    #cls=GlobalArgs,
    name = 'kraken2', help='Reads based analysis (kraken2) model',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')
@options.add_options(options.global_options_list)
#@options.add_options(options.input_fastq_options)
@options.add_options(options.output_options)
@options.add_options(options.kraken2_options)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)
        print(key, value)

    advanced_options = utilities.parse_unknown(ctx.args, 'kraken2')
    setattr(args, 'advanced_options', advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'kraken2', temp_output_files)
    
    reads_based_analyse(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Reads Based Analysis Model complete in %ss'%(str(end-start)))
    logger.info('MVF Reads Based Analysis Model complete in %ss'%(str(end-start)))


def run_kraken2(kraken2, reads1, reads2, output, report, database, advanced_options, logger, reads_based_log, num_threads):
    kraken2_command = [kraken2, '--threads', num_threads]
    kraken2_command += ['--db', database]
    kraken2_command += ['--output', output, '--report', report]
    kraken2_command += ['--paired',  reads1, reads2]
    if advanced_options is not None:
        kraken2_command += advanced_options

    logger.info("Command: " + ' '.join(kraken2_command))
    with open(reads_based_log, 'w') as logfile:
        subprocess.run(kraken2_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def get_percentage(df):
    sum_reads = df.loc[0, 'sum reads']
    result = pd.DataFrame(columns=['taxid', 'abundance', 'name'])
    print(df.loc[0])
    for i in range(len(df)):
        result.loc[len(result)] = ({
            'taxid': df.loc[i, 'taxid'],
            'abundance': round(df.loc[i, 'reads'] / sum_reads, 4) * 100,
            'name': df.loc[i, 'name'].strip()
            })
    return result

def find_virus(kraken2_report_path, virus_abundance_path):
    kraken2_output = pd.read_csv(kraken2_report_path, sep='\t', header= None, names=['percentage', 'sum reads', 'reads', 'rank', 'taxid', 'name'])
    #kraken2_output.columns = ['percentage', 'sum reads', 'reads', 'rank', 'taxid', 'name']
    kraken2_virus = pd.DataFrame(columns=kraken2_output.columns)
    flag = 0
    for i in range(len(kraken2_output)):
        rank = kraken2_output.loc[i, 'rank'].strip()
        name = kraken2_output.loc[i, 'name'].strip()
        if rank == 'D' and name == 'Viruses':
            flag = 1
        if rank == 'D' and name != 'Viruses':
            flag = 0

        if flag == 1:
            kraken2_virus.loc[len(kraken2_virus)] = kraken2_output.loc[i]
    kraken2_virus = get_percentage(kraken2_virus)
    kraken2_virus.to_csv(virus_abundance_path, sep='\t', index=False)
            

def reads_based_analyse(args):
    outdir = args.kraken2_dir
    advanced_options = find_advanced_options('kneaddata', args)
    
    try:
        run_kraken2(
            args.kraken2_exe,
            args.input1, args.input2,
            args.kraken2_output, args.kraken2_report,
            args.kraken2_database,
            advanced_options,
            logger, args.kraken2_log,
            args.threads
            )
        print("Kraken2 output saved in %s"%(outdir))
        logger.info("Kraken2 output saved in %s"%(outdir))
        find_virus(args.kraken2_report, os.path.join(outdir, 'kraken2.virus_abundance.txt'))
        print("Kraken2 virus abundance file saved in %s"%(outdir))
        logger.info("Kraken2 virus abundance file in %s"%(outdir))

    except Exception as e:
        print("ERROR: Kraken2 Fail!")
        logger.error(traceback.format_exc())
        logger.error("ERROR: Kraken2 Fail!")
        sys.exit()