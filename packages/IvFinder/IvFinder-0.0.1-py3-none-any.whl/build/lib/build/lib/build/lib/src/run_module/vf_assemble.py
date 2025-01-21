import os
import sys
import time
BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )
import shutil
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
    name = 'assemble', help='Contigs Assembly model',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.help_option('--help', '-h', help='Show this message and exit')
#@options.add_options(options.input_fastq_options)
@options.add_options(options.assemble_input_list)

@options.add_options(options.assemble_options_list)
@options.add_options(options.contig_filter_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)

    advanced_options = utilities.parse_unknown(ctx.args, 'assemble')
    setattr(args, 'advanced_options', advanced_options)

    temp_output_files = []
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    utilities.update_configuration(args, 'assemble', temp_output_files, 'separated')
    
    assemble(args)

    for file in temp_output_files:
        utilities.remove_file(file)

    end = time.time()
    print('MVF Assemble Model Complete in %ss'%(str(end-start)))
    logger.info('MVF Assemble Model Complete in %ss'%(str(end-start)))

def run_assemble(assembler, reads1, reads2, outdir, memory, advanced_options, logger, assemble_log, num_threads):
    assemble_command = [assembler]
    assemble_command += ['-t', num_threads]
    assemble_command += ['-1', reads1, '-2', reads2]
    assemble_command += ['-o', outdir]
    assemble_command += ['-m', memory]
    if advanced_options is not None:
        assemble_command += advanced_options

    print(assemble_command)
    logger.info("Excute command: " + ' '.join(assemble_command))
    with open(assemble_log, 'w') as logfile:
        subprocess.run(assemble_command, shell=False, check=True, stderr=subprocess.STDOUT, stdout=logfile)

def assemble(args):
    outdir = args.assemble_dir
    
    advanced_options = find_advanced_options('assemble', args)
    try:
        subprocess.run(['rm', '-fR', outdir], shell=False, check=True)
        run_assemble(
            args.assemble_exe,
            args.input1, args.input2,
            outdir,
            args.memory,
            advanced_options,
            logger, args.assemble_log,
            args.threads
        )
        if args.assembler == 'megahit':
            contigs = os.path.join(outdir, 'final.contigs.fa')
            os.rename(os.path.join(outdir, 'final.contigs.fa'), os.path.join(outdir, 'final_assembly.fasta'))
        elif args.assembler == 'metaspades':
            contigs = os.path.join(outdir, 'scaffolds.fasta')
            os.rename(os.path.join(outdir, 'scaffolds.fasta'), os.path.join(outdir, 'final_assembly.fasta'))
        
        '''run_reformat(
            args.reformat_exe,
            contigs,
            os.path.join(outdir, 'reformat.contigs.fa'),
            str(args.raw_memory * 1000) + 'm',
            'nucl',
            str(args.min_contig_len),
            str(args.max_contig_len),
            logger, args.assemble_filter_log
        )

        if args.min_contig_id != 0 or args.min_contig_coverage != 0:
            run_cdhit(
                args.cdhit_exe,
                os.path.join(outdir, 'reformat.contigs.fa'),
                os.path.join(outdir, 'cdhit.contigs.fa'),
                str(args.raw_memory * 1000),
                str(get_word_size(args.min_contig_id, 'nucl')),
                str(args.min_contig_id),
                str(args.min_contig_coverage),
                logger, args.assemble_filter_log,
                args.threads
            )
            os.rename(os.path.join(outdir, 'cdhit.contigs.fa'), os.path.join(outdir, 'final_assembly.fasta'))
            os.unlink(os.path.join(outdir, 'reformat.contigs.fa'))
        else:
            os.rename(os.path.join(outdir, 'reformat.contigs.fa'), os.path.join(outdir, 'final_assembly.fasta'))'''

        logger.info("Reads assembly complete by %s, output saved in %s"%(args.assembler.title(), outdir))
        print("Reads assembly complete by %s, output saved in %s"%(args.assembler.title(), outdir))
        return True
    except Exception as e:
        logger.error("Error: %s Fail!"%(args.assembler.title()))
        logger.error(traceback.format_exc())
        print("Error: %s Fail!"%(args.assembler.title()))
        sys.exit()
        