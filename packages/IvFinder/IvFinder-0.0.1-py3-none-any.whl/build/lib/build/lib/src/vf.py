import os
import sys

BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )
import multiprocessing
import traceback
import time
from src.run_module import *
from src.configs import options
import click_option_group
import logging
import click
import argparse
import atexit
import warnings
warnings.filterwarnings("ignore")

logger=logging.getLogger(__name__)

@click.help_option('-h', '--help', help='Show this message and exit')

@click.group()
def entry_point():
    pass

@click.command(
    #cls=global_args.GlobalArgs,
    name = 'whole', help='Run the whole pipeline, default: readsqc, assemble, orf_predict, annotate, quantity, report',
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
#@add_options(vf_assemble.assemble_command)
@options.add_options(options.main_input_list)
@options.add_options(options.main_options_list)
@options.add_options(options.readsqc_options_list)
@options.add_options(options.assemble_options_list)
@options.add_options(options.contig_filter_list)
@options.add_options(options.filter_options_list)
@options.add_options(options.annotate_options_list)
@options.add_options(options.CAT_options_list)
@options.add_options(options.global_options_list)

@click.pass_context
def main(ctx, *args, **kwargs):
    start = time.time()
    args = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(args, key, value)
    #@options.readsqc_options[0].
    #print(click_option_group.OptionGroup.get_option_names(ctx=options.readsqc_config))
    print(kwargs)
    print(ctx)
    test = options.main_input_options.get_options(ctx)
    print(dict(test))
    temp_output_files = []
    main_step = [x.strip() for x in args.step.split(',')]
    #utilities.update_configuration(args, main_step, temp_output_files)
    utilities.setup_global_settings(args)
    utilities.setup_logging(args)
    atexit.register((lambda: utilities.remove_file(temp_output_files)))
    if args.not_contig_filter:
        args.is_contig_filter = False

    if 'readsqc' in main_step:
        if len(list(args.input)) == 2:
            if not args.bypass_trim:
                readsqc_args = argparse.Namespace()
                readsqc_args = utilities.update_configuration(args, 'readsqc', temp_output_files, 'whole')
                print(readsqc_args)
                advanced_options = utilities.parse_unknown(ctx.args, 'readsqc')
                setattr(readsqc_args, 'advanced_options', advanced_options)
                
                vf_readsqc.quality_control(readsqc_args)
                #subprocess.run(readsqc_command, shell=False, check=True)
                #for file in temp_output_files:
                    #utilities.remove_file(file)
            else:
                logger.info("Bypass Trim was set! Skip Readsqc Model!")
        else:
            logger.error("Error: Readsqc need two sequence reads! Cannot run Readsqc Model!")
            sys.exit("Error: Readsqc need two sequence reads! Cannot run Readsqc Model!")
    
    if 'assemble' in main_step:
        if len(list(args.input)) == 2:
            assemble_args = argparse.Namespace()
            assemble_args = utilities.update_configuration(args, 'assemble', temp_output_files, 'whole')
            advanced_options = utilities.parse_unknown(ctx.args, 'assemble')
            setattr(assemble_args, 'advanced_options', advanced_options)

            vf_assemble.assemble(assemble_args)
            #subprocess.run(assemble_command, shell=False, check=True)
        else:
            logger.error("Error: Assemble need two sequence reads! Cannot run Assemble Model!")
            sys.exit("Error: Assemble need two sequence reads! Cannot run Assemble Model!")

    if not args.not_contig_filter and 'filter' in main_step:
        args.is_contig_filter = True
        #setattr(args, 'nucl', args.contigs)
        setattr(args, 'seq_type', 'nucl')
        contigs_filter_args = argparse.Namespace()
        contigs_filter_args = utilities.update_configuration(args, 'filter', temp_output_files, 'whole')
        vf_filter.filter(contigs_filter_args)


    if 'orf_predict' in main_step:
        orf_predict_args = argparse.Namespace()
        orf_predict_args = utilities.update_configuration(args, 'orf_predict', temp_output_files, 'whole')
        advanced_options = utilities.parse_unknown(ctx.args, 'orf_predict')
        setattr(orf_predict_args, 'advanced_options', advanced_options)

        vf_orf_predict.orf_predict(orf_predict_args)

            
    if 'filter' in main_step:
        args.is_contig_filter = False
        setattr(args, 'seq_type', 'prot')
        filter_args = argparse.Namespace()
        filter_args = utilities.update_configuration(args, 'filter', temp_output_files, 'whole')
        vf_filter.filter(filter_args)


    if 'annotate' in main_step:
        annotate_args = argparse.Namespace()
        annotate_args = utilities.update_configuration(args, 'annotate', temp_output_files, 'whole')
        advanced_options = utilities.parse_unknown(ctx.args, 'annotate')
        setattr(annotate_args, 'advanced_options', advanced_options)

        vf_annotate.annotate(annotate_args)
        

    if 'quantify' in main_step:
        if len(list(args.input)) == 2:
            quantify_args = argparse.Namespace()
            quantify_args = utilities.update_configuration(args, 'quantify', temp_output_files, 'whole')
            index_advanced_options = utilities.parse_unknown(ctx.args, 'index')
            quant_advanced_options = utilities.parse_unknown(ctx.args, 'quant')
            if index_advanced_options and quant_advanced_options:
                setattr(quantify_args, 'advanced_options', index_advanced_options.update(quant_advanced_options))
            elif index_advanced_options:
                setattr(quantify_args, 'advanced_options', index_advanced_options)
            else:
                setattr(quantify_args, 'advanced_options', quant_advanced_options)

            vf_quantify.quantify(quantify_args)
        else:
            logger.error("Error: Quantify need two sequence reads! Cannot run Quantify Model!")
            sys.exit("Error: Quantify need two sequence reads! Cannot run Quantify Model!")

    if 'report' in main_step:
        report_args = argparse.Namespace()
        report_args = utilities.update_configuration(args, 'report', temp_output_files, 'whole')

            
        vf_report.generate_report(
            report_args.virus_anno, report_args.nonvirus_anno,
            report_args.orf, report_args.contigs, report_args.quant,
            report_args.cluster_rep, report_args.cluster_file,
            report_args.one_minus_r,
            report_args.report_dir,
            report_args.report_log,
            report_args.processes
        )

    #for file in temp_output_files:
        #utilities.remove_file(file)
    utilities.remove_file(temp_output_files)
    end = time.time()
    print('MVF complete in %s s'%(str(end-start)))
    logger.info('MVF complete in %s s'%(str(end-start)))

entry_point.add_command(main)
entry_point.add_command(vf_readsqc.main)
entry_point.add_command(vf_assemble.main)
entry_point.add_command(vf_filter.main)
entry_point.add_command(vf_orf_predict.main)
entry_point.add_command(vf_annotate.main)
entry_point.add_command(vf_quantify.main)
entry_point.add_command(vf_report.main)
#entry_point.add_command(vf_kraken2.main)

if __name__ == "__main__":
    entry_point()