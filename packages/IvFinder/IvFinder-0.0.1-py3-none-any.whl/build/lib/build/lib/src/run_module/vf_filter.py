import os
import sys
import time
BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )

import shlex
import subprocess
import traceback
import argparse
from .find_options import find_advanced_options
import utilities
import click
from click_option_group import optgroup
from configs import options
from configs import config
from intervals import FloatInterval
from Bio import SeqIO
import decimal
import logging

logger=logging.getLogger(__name__)

@click.command(
    #cls=GlobalArgs,
    name = 'filter', help='remove redundance',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)

@click.help_option('--help', '-h', help='Show this message and exit')
@options.add_options(options.filter_input_list)

@options.add_options(options.filter_options_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)


    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    setattr(args, 'is_contig_filter', False)
    utilities.update_configuration(args, 'filter', temp_output_files, 'separated')

    filter(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Filter Model Complete in %ss'%(str(end-start)))
    logger.info('MVF Filter Model Complete in %ss'%(str(end-start)))

def get_word_size(min_id, seq_type):
    if seq_type == 'prot':
        if min_id in FloatInterval.closed(0.7, 1.0):
            return 5
        elif min_id in FloatInterval.closed_open(0.6, 0.7):
            return 4
        elif min_id in FloatInterval.closed_open(0.5, 0.6):
            return 3
        elif min_id in FloatInterval.closed_open(0.4, 0.5):
            return 2
        else:
            print("ERROR: CD-HIT cannot cluster with %s identity!"%(str(min_id)))
            logger.error("ERROR: CD-HIT cannot cluster with %s identity!"%(str(min_id)))
            sys.exit()
    elif seq_type == 'nucl':
        if min_id in FloatInterval.closed(0.95, 1.0):
            return 10
        elif min_id in FloatInterval.closed_open(0.9, 0.95):
            return 8
        elif min_id in FloatInterval.closed_open(0.88, 0.9):
            return 7
        elif min_id in FloatInterval.closed_open(0.85, 0.88):
            return 6
        elif min_id in FloatInterval.closed_open(0.8, 0.85):
            return 5
        elif min_id in FloatInterval.closed_open(0.75, 0.8):
            return 4
        else:
            print("ERROR: CD-HIT cannot cluster with %s identity!"%(str(min_id)))
            logger.error("ERROR: CD-HIT cannot cluster with %s identity!"%(str(min_id)))
            sys.exit()

def run_reformat(reformat, query, outdir, memory, seq_type,min_len, max_len, logger, filter_log):
    reformat_command = [reformat]
    reformat_command += ['in='+query, 'out='+outdir]
    reformat_command += ['minlength='+min_len, 'maxlength='+max_len]
    if seq_type == 'prot':
        reformat_command += ['amino=t']
    reformat_command += ['-Xmx'+memory]

    logger.info("Command: " + ' '.join(reformat_command))
    with open(filter_log, 'w') as logfile:
        subprocess.run(reformat_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)


def run_cdhit(cdhit, query, outdir, memory, word_size, min_id, min_coverage, logger, filter_log, num_threads):
    cdhit_command = [cdhit]
    cdhit_command += ['-T', num_threads, '-M', memory]
    #cdhit_command += ['-T', num_threads]
    cdhit_command += ['-i', query, '-o', outdir]
    cdhit_command += ['-n', word_size]
    if decimal.Decimal(min_id) > 0:
        cdhit_command += ['-c', min_id]
    
    if decimal.Decimal(min_coverage) > 0:
        cdhit_command += ['-aL', min_coverage]
    cdhit_command += ['-d', '0']

    logger.info("Command: " + ' '.join(cdhit_command))
    with open(filter_log, 'a') as logfile:
        subprocess.run(cdhit_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def reference_filter(reference, input_seq, output_seq):
    ref = SeqIO.index(reference, 'fasta')
    file_in = SeqIO.index(input_seq, 'fasta')
    file_out = open(output_seq, 'w')
    for seq_index in ref:
        if seq_index in file_in:
            file_out.write(file_in[seq_index].format('fasta'))
    ref.close()
    file_in.close()
    file_out.close()

def filter(args):
    outdir = args.filter_dir
    '''
    filter_log = args.assemble_filter_log if args.is_contig_filter else args.filter_log
    min_len = args.min_contig_len if args.is_contig_filter else args.min_len
    max_len = args.max_contig_len if args.is_contig_filter else args.max_len
    min_id = args.min_contig_id if args.is_contig_filter else args.min_id
    min_coverage = args.min_contig_coverage if args.is_contig_filter else args.min_coverage'''


    try:
        run_reformat(
            args.reformat_exe,
            args.filter_in,
            args.reformat_out,
            str(args.memory * 1000) + 'm',
            args.seq_type,
            str(args.min_len),
            str(args.max_len),
            logger, args.filter_log
        )

        if args.min_id != 0 or args.min_coverage != 0:
            run_cdhit(
                args.cdhit_exe,
                args.reformat_out,
                args.filter_out,
                str(args.memory * 1000),
                str(get_word_size(args.min_id, args.seq_type)),
                str(args.min_id),
                str(args.min_coverage),
                logger, args.filter_log,
                args.threads
            )
            os.unlink(args.reformat_out)

        else:
            os.rename(args.reformat_out, args.filter_out)

        if args.is_contig_filter:
            os.rename(args.filter_out, os.path.join(outdir, 'final_assembly_filtered.fasta'))
            if os.path.exists(args.filter_out+'.clstr'):
                os.rename(args.filter_out+'.clstr', os.path.join(outdir, 'final_assembly_filtered.fasta.clstr'))
        
        if 'filter_in_another' in args:
            reference_filter(args.filter_out, args.filter_in_another, args.filter_out_another)
            
        print("Filter output saved in %s"%(outdir))
        logger.info("Filter output saved in %s"%(outdir))
        return True
    except Exception as e:
        print("ERROR: Filter Fail!")
        logger.error(traceback.format_exc())
        logger.error("ERROR: Filter Fail!")
        sys.exit()