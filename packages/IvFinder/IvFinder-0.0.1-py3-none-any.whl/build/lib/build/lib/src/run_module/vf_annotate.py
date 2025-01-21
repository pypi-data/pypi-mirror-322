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
#from ..configs.global_args import GlobalArgs
from configs import options
from configs import config

import logging

logger=logging.getLogger(__name__)

@click.command(
    #cls=GlobalArgs,
    name = 'annotate', help='Annotate sequences model',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')
@options.add_options(options.annotate_input_list)
#@options.add_options(options.output_options)
@options.add_options(options.annotate_options_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)

    advanced_options = utilities.parse_unknown(ctx.args, 'annotate')
    setattr(args, 'advanced_options', advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'annotate', temp_output_files, 'separated')
    
    annotate(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Annotate Model Complete in %s s'%(str(end-start)))
    logger.info('MVF Annotate Model Complete in %s s'%(str(end-start)))


def run_blast(annotate_exe, db, out, query, params, advanced_options, logger, anno_log, num_threads):
    blast_command = [annotate_exe] 
    blast_command += ['-num_threads', num_threads]
    blast_command += shlex.split(params)
    blast_command += ['-db', db, '-query', query, '-out', out]

    if advanced_options is not None:
        blast_command += advanced_options

    logger.info("Command: " + ' '.join(blast_command))
    with open(anno_log, 'w') as logfile:
        subprocess.run(blast_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)


def run_diamond(annotate_exe, blast_type, db, out, query, params, advanced_options, logger, anno_log, num_threads):
    diamond_command = [annotate_exe, blast_type]
    diamond_command += ['-p', num_threads]
    diamond_command += shlex.split(params)
    diamond_command += ['-d', db, '-q', query, '-o', out]
 
    if advanced_options is not None:
        diamond_command += advanced_options
    
    logger.info("Command: " + ' '.join(diamond_command))
    with open(anno_log, 'a') as logfile:
        subprocess.run(diamond_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)


def annotate(args):
    outdir = args.annotate_dir
    advanced_options=find_advanced_options('annotate', args)
    
    if args.diamond:
        logger.info('Identifying coding regions using Diamond ' + args.blast_type)
        try:
            if args.virus:
                run_diamond(
                    args.annotate_exe, args.blast_type,
                    args.virus,
                    args.virus_anno,
                    args.query,
                    config.diamond_params,
                    advanced_options,
                    logger, args.annotate_log,
                    args.threads
                )
                print("Virus Diamond output saved in %s"%(outdir))
                logger.info("Virus Diamond output saved in %s"%(outdir))
            else:
                print("No Virus Database Find")
                logger.info("No Virus Database Find")
            
            if args.non_virus:
                run_diamond(
                    args.annotate_exe, args.blast_type,
                    args.non_virus,
                    args.nonvirus_anno,
                    args.query,
                    config.diamond_params,
                    advanced_options,
                    logger, args.annotate_log,
                    args.threads
                )
                print("Non-Virus Diamond output saved in %s"%(outdir))
                logger.info("Non-Virus Diamond output saved in %s"%(outdir))
            else:
                print("No Non-Virus Database Find")
                logger.info("No Non-Virus Database Find")

            return True
        except Exception as e:
            print("ERROR: Diamond Fail!")
            logger.error(traceback.format_exc())
            logger.error("ERROR: Diamond Fail!")
            sys.exit()
    else:
        logger.info('Identifying coding regions using '+args.blast_type)
        try:
            if args.virus:
                run_blast(
                    args.annotate_exe, args.blast_type,
                    args.virus,
                    args.virus_anno,
                    args.query,
                    config.blast_params,
                    advanced_options,
                    logger, args.annotate_log,
                    args.threads
                )
                print("Virus Diamond output saved in %s"%(outdir))
                logger.info("Virus Diamond output saved in %s"%(outdir))
            else:
                print("No Virus Database Find")
                logger.info("No Virus Database Find")
            
            if args.non_virus:
                run_blast(
                    args.annotate_exe, args.blast_type,
                    args.non_virus,
                    args.nonvirus_anno,
                    args.query,
                    config.blast_params,
                    advanced_options,
                    logger, args.annotate_log,
                    args.threads
                )
                print("Non-Virus Blast output saved in %s"%(outdir))
                logger.info("Non-Virus Blast output saved in %s"%(outdir))
            else:
                print("No Non-Virus Database Find")
                logger.info("No Non-Virus Database Find")
            return True
        except:
            print("ERROR: Blast Fail!")
            logger.error("ERROR: Blast Fail!")
            sys.exit()