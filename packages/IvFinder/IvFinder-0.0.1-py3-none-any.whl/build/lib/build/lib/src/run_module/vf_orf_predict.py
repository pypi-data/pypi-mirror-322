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
    name = 'orf_predict', help='Orf prediction model',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')

@options.add_options(options.orf_predict_input_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)
        print(key, value)

    advanced_options = utilities.parse_unknown(ctx.args, 'orf_predict')
    setattr(args, 'advanced_options', advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'orf_predict', temp_output_files, 'separated')
    
    orf_predict(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF ORF Prediction Model Complete in %ss'%(str(end-start)))
    logger.info('MVF ORF Prediction Model Complete in %ss'%(str(end-start)))


def run_prodigal(prodigal, contigs, aa_predict, nuc_predict, gff_predict, advanced_options, logger, gp_log):
    prodigal_command = [prodigal]
    prodigal_command += ['-i', contigs]
    prodigal_command += ['-a', aa_predict, '-d', nuc_predict, '-o', gff_predict]
    prodigal_command += ['-f', 'gff', '-p', 'meta']
    if advanced_options is not None:
        prodigal_command += advanced_options

    print(prodigal_command)
    logger.info("Command: " + ' '.join(prodigal_command))
    with open(gp_log, 'w') as logfile:
        subprocess.run(prodigal_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def orf_predict(args):
    outdir = args.orf_predict_dir
    advanced_options = find_advanced_options('orf_predict', args)
        
    try:
        run_prodigal(
            args.predict_exe,
            args.contigs,
            args.predict_aa, args.predict_nuc, args.predict_gff,
            advanced_options,
            logger, args.orf_predict_log
        )
        print("Prodigal output saved in %s"%(outdir))
        logger.info("Prodigal output saved in %s"%(outdir))
        return True
    except Exception as e:
        print("ERROR: Prodigal Fail!")
        logger.error(traceback.format_exc())
        logger.error("ERROR: Prodigal Fail!")
        sys.exit()