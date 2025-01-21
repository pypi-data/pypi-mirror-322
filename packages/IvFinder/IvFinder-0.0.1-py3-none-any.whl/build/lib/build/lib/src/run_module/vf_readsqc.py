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
import importlib_resources
#from ..configs.global_args import GlobalArgs
from configs import options
from configs import config
import logging

logger=logging.getLogger(__name__)

@click.command(
    #cls=GlobalArgs,
    name = 'readsqc', help='Quanlity control model',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')
@options.add_options(options.readsqc_input_list)

@options.add_options(options.readsqc_options_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)

    advanced_options = utilities.parse_unknown(ctx.args, 'readsqc')
    setattr(args, 'advanced_options', advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'readsqc', temp_output_files, 'separated')

    quality_control(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Reads QC Model Complete in %ss'%(str(end-start)))
    logger.info('MVF Reads QC Model Complete in %ss'%(str(end-start)))


def run_kneaddata(kneaddata,reads1,reads2,database,outdir,memory,advanced_options,logger,qc_log,num_threads,num_processes):
    data_path = importlib_resources.files("data")
    trimmomatic_path = str(data_path / 'Trimmomatic-0.33')
    print(trimmomatic_path)
    kneaddata_command = [kneaddata]
    kneaddata_command += ['-t', num_threads, '-p', num_processes, '--bypass-trf']
    kneaddata_command += ['-i1', reads1, '-i2', reads2]
    kneaddata_command += ['--output', outdir]
    kneaddata_command += ['--max-memory', memory]
    kneaddata_command += ['--trimmomatic', trimmomatic_path]
    #kneaddata_command += ['--bowtie2', bowtie2_path]
    for i in range(len(database)):
        kneaddata_command += ['-db', database[i]]
    kneaddata_command += ['--trimmomatic-options="LEADING:20"',  '--trimmomatic-options="TRAILING:20"', '--trimmomatic-options="MINLEN:90"']
    kneaddata_command += ['--output-prefix', 'kneaddata', '--reorder']

    if advanced_options is not None:
        kneaddata_command += advanced_options
    
    print(kneaddata_command)
    logger.info("Excute command: " + ' '.join(kneaddata_command))
    with open(qc_log, 'w') as logfile:
        subprocess.run(kneaddata_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def quality_control(args):
    outdir = args.readsqc_dir
    advanced_options = find_advanced_options('readsqc', args)

    try:
        run_kneaddata(
            args.readsqc_exe,
            args.input1, args.input2,
            args.host,
            outdir,
            args.memory,
            advanced_options, 
            logger, args.readsqc_log,
            args.threads, args.processes
        )
        print("Readsqc output saved in %s"%(outdir))
        logger.info("Readsqc output saved in %s"%(outdir))
        return True
    except Exception as e:
        print("ERROR: Kneaddata Fail!")
        logger.error(traceback.format_exc())
        logger.error("ERROR: Kneaddata Fail!")
        sys.exit()
  
