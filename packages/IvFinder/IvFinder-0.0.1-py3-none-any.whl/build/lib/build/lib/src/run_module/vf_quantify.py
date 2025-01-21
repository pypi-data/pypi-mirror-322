import os
import sys
import time
BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )

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
    name = 'quantify', help='Quantify genes',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')

@options.add_options(options.quantify_input_list)
@options.add_options(options.quantify_options_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)

    index_advanced_options = utilities.parse_unknown(ctx.args, 'index')
    quant_advanced_options = utilities.parse_unknown(ctx.args, 'quant')
    if index_advanced_options and quant_advanced_options:
        setattr(args, 'advanced_options', index_advanced_options.update(quant_advanced_options))
    elif index_advanced_options:
        setattr(args, 'advanced_options', index_advanced_options)
    else:
        setattr(args, 'advanced_options', quant_advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'quantify', temp_output_files, 'separated')
    
    quantify(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Quantify Model Complete in %ss'%(str(end-start)))
    logger.info('MVF Quantify Model Complete in %ss'%(str(end-start)))

def run_salmon(salmon, reads1, reads2, query, quant_index, outdir, index_advanced_options, quant_advanced_options, logger, quant_log, num_threads):
    salmon_index_command = [salmon, 'index', '-t', query, '-i', quant_index]
    if index_advanced_options is not None:
        salmon_index_command += index_advanced_options

    logger.info("Command: " + ' '.join(salmon_index_command))
    with open(quant_log, 'w') as logfile:
        subprocess.run(salmon_index_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)
    logger.info("Salmon index saved in " + quant_index)

    salmon_command = [salmon, 'quant', '-l', 'A', '-i', quant_index, '-p', num_threads]
    salmon_command += ['-1', reads1, '-2', reads2]
    salmon_command += ['-o', outdir]
    salmon_command += ['--validateMappings', '--meta', '--minAssignedFrags', '1']
    if quant_advanced_options is not None:
        salmon_command += quant_advanced_options

    logger.info("Command: " + ' '.join(salmon_command))
    with open(quant_log, 'a') as logfile:
        subprocess.run(salmon_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def run_bwa(bwa, reads1, reads2, query, quant_index, outdir, badvanced_options, logger, quant_log, num_threads):
    out_sam = os.path.join(outdir, quant_index+'.sam')
    out_bam = os.path.join(outdir, quant_index+'.bam')
    bwa_index_command = [bwa, 'index' , '-p', quant_index, query]
    logger.info("Command: " + ' '.join(bwa_index_command))
    with open(quant_log, 'w') as logfile:
        subprocess.run(bwa_index_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)
    logger.info("BWA index saved in " + quant_index)

    bwa_command = [bwa, 'mem', '-t', num_threads]
    bwa_command += [quant_index, reads1, reads2]
    bwa_command += ['-o', out_sam]
    with open(quant_log, 'w') as logfile:
        subprocess.run(bwa_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)
    logger.info("BWA SAM saved in " + outdir)
    

def quantify(args):
    outdir = args.quantify_dir
    index_advanced_options = find_advanced_options('index', args)
    quant_advanced_options = find_advanced_options('quant', args)

    try:
        run_salmon(
            args.quant_exe,
            args.input1, args.input2,
            args.reference, args.quant_index,
            outdir,
            index_advanced_options, quant_advanced_options,
            logger, args.quantify_log,
            args.threads
        )
        print("Salmon output saved in " + outdir)
        logger.info("Salmon output saved in " + outdir)
        return True
    except:
        print("Salmon Fail")
        logger.error(traceback.format_exc())
        logger.error("Salmon Fail!")
        sys.exit()