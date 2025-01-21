import os
import sys
import fnmatch
import shutil
import multiprocessing
import tempfile
import gzip
from concurrent.futures import ProcessPoolExecutor, as_completed
from configs import config
import logging
import argparse

logger=logging.getLogger(__name__)

def parse_unknown(unparsed, command):
    advanced_options = dict()
    i = 0
    while i < len(unparsed):
        if command not in unparsed[i]:
            i += 1
            continue

        temp_args = unparsed[i][2:].split(command, 1)
        print(temp_args)
        option = [temp_args[-1]]

        if option == '--bowtie2-options' or option == '--trimmomatic-options':
            option += ['=\"' + unparsed[i+1] + '\"']
            i += 2
        else:
            if i+1 < len(unparsed) and unparsed[i+1][:2] != '--':
                option += [unparsed[i+1]]
                i += 2
            else:
                i += 1
    
        if command not in advanced_options:
            advanced_options[command] = option
        else:
            advanced_options[command] += option

    return advanced_options

def create_directory(directory):
    if not os.path.exists(directory):
        logger.debug("Creating output directory: "+directory)
        try:
            os.makedirs(directory)
        except EnvironmentError:
            message="Unable to create output directory: " + directory
            logger.critical(message)
            sys.exit(message)


def remove_file(temp_files):
    #Try to remove the file
    for file in temp_files:
        try:
            logger.info('Try to remove: ' + file)
            os.unlink(file)
        except EnvironmentError:
            print("Unable to remove file: " + file)
            logger.warning("Unable to remove file: " + file)

def get_file_name(file):
    return os.path.splitext(os.path.basename(file))[0]

def gunzip_file(gzip_file, new_file):
    message="Decompress gzip file"
    print(message+"\n")
    logger.info(message)  

    try:
        file_handle_gzip=gzip.open(gzip_file,"rt")
        # write the gunzipped file
        file_handle=open(new_file,"w")
        shutil.copyfileobj(file_handle_gzip, file_handle)
    except EnvironmentError:
        sys.exit("Critical Error: Unable to gunzip input file: " + gzip_file)
    finally:
        file_handle.close()
        file_handle_gzip.close()
        
    logger.info("Decompressed file created: " + new_file)
    return new_file

def decompress_file(file, output_folder, temp_file_list):
    if file.endswith(".gz"):
        file_name = get_file_name(file)
        file_out, new_file = tempfile.mkstemp(
            prefix="decompressed_",
            suffix="_" + file_name,
            dir=output_folder
        )
        os.close(file_out)
        gunzip_file(file, new_file)
        temp_file_list.append(new_file)
    else:
        new_file = file

    return new_file



def check_sequence_identifier_format(file):
    """ Check the fastq file to see if there are spaces in the identifier
        and the format of the id to see if this is the new illumina format """ 
    
    #checking first 100 (400/4) lines
    num_seq_to_check=100 
    
    new_format = False
    with open(file, 'rt') as file_handle:
        NR = 0  #count read lines
        for line in file_handle:
            if NR % 4 == 0:
                seq_id = line
                if " " in seq_id:
                    new_format=True
                if not seq_id.endswith("/1\n") and not seq_id.endswith("/2\n"):
                    new_format=True
                #print(seq_id)
            if NR >= num_seq_to_check:
                break
            NR += 1
    
    file_handle.close()
    
    return new_format
   
        
def get_reformatted_identifiers(file, input_index, output_folder, temp_file_list):
    """ Reformat the sequence identifiers in the fastq file writing to a temp file """
    
    input_file = decompress_file(file, output_folder, temp_file_list)

    # check if the file needs to be reformatted
    reformat_file=check_sequence_identifier_format(input_file)
    
    if not reformat_file:
        return input_file
    
    message="Reformatting file sequence identifiers"
    print(message+"\n")
    logger.info(message)   
    
    file_name = get_file_name(file)
    file_out, new_file = tempfile.mkstemp(
        prefix = "reformatted_identifiers",
        suffix="_" + file_name,
        dir = output_folder
    )
    os.close(file_out)
    
    with open(new_file, "wt") as file_handle:
        with open(input_file, 'rt') as file:
            NR = 0
            for line in file:
                # reformat the identifier and write to temp file
                if NR % 4 == 0:
                    if " 1:" in line:
                        line=line.replace(" 1","").rstrip()+"#0/1\n"
                    elif " 2:" in line:
                        line=line.replace(" 2","").rstrip()+"#0/2\n"
                    elif " " in line:
                        line=line.replace(" ","")
                    if not line.endswith("/1\n") and not line.endswith("/2\n"):  
                        if (input_index == 1):
                            line = line.rstrip()+"#0/1\n"
                        else:
                            line = line.rstrip()+"#0/2\n"      
                    file_handle.write("".join(line))
                else:
                    file_handle.write(line)
                NR += 1
    

    # add the new file to the list of temp files
    temp_file_list.append(new_file)
    
    return new_file

def is_exe(exe):
    return os.path.isfile(exe) and os.access(exe, os.X_OK)

def find_dependency(path_provided, exe, name):
    if path_provided:
        path_provided = os.path.abspath(path_provided)
        try:
            files = os.listdir(path_provided)
        except:
            sys.exit('ERROR: Unable to list files in {0} directory: {1}'.format(name, path_provided))

        found_paths = fnmatch.filter(files, exe)
        if not found_paths:
            sys.exit('ERROR: The {0} executable is not included in the directory: {1}'.format(exe, path_provided))
        else:
            exe_file = os.path.join(path_provided, found_paths[0])
            
            if is_exe(os.path.abspath(exe_file)):
                dependency_path = exe_file
                return dependency_path
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('')
            exe_file = os.path.join(path, exe)
            if is_exe(exe_file):
                dependency_path = exe_file
                return dependency_path
            
    sys.exit('ERROR: Unable to find {0}'.format(name))

def setup_global_settings(args):
    args.output_dir = os.path.abspath(args.output_dir)
    create_directory(args.output_dir)

    if args.threads > multiprocessing.cpu_count():
        args.threads = 1

    args.threads = str(args.threads)
    args.processes = str(args.processes)
    if 'raw_memory' not in args:
        if 'memory' in args:
            setattr(args, 'raw_memory', args.memory)

def setup_logging(args):
    if not args.logs_dir:
        args.logs_dir = os.path.join(args.output_dir, config.logs_dir)
        create_directory(args.logs_dir)
    else:
        args.logs_dir = os.path.abspath(args.logs_dir)
    
    setattr(args, 'main_log', os.path.join(args.logs_dir, 'main.log'))
    setattr(args, 'kraken2_log', os.path.join(args.logs_dir, 'kraken2.log'))
    setattr(args, 'readsqc_log', os.path.join(args.logs_dir, 'reads_qc.log'))
    setattr(args, 'assemble_log', os.path.join(args.logs_dir, 'assemble.log'))
    setattr(args, 'assemble_filter_log', os.path.join(args.logs_dir, 'assemble_filter.log'))
    setattr(args, 'filter_log', os.path.join(args.logs_dir, 'filter.log'))
    setattr(args, 'orf_predict_log', os.path.join(args.logs_dir, 'orf_prediction.log'))
    setattr(args, 'annotate_log', os.path.join(args.logs_dir, 'annotation.log'))
    setattr(args, 'quantify_log', os.path.join(args.logs_dir, 'quantify.log'))
    setattr(args, 'report_log', os.path.join(args.logs_dir, 'report.log'))

    logging.basicConfig(
        level = getattr(logging, "DEBUG"),
        filename = args.main_log,
        filemode = 'w',
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt= "%Y-%m-%d %H:%M:%S %p"
    )
    logger.info("Run MVF")
    logger.info("Output files will be written to: {0}".format(args.output_dir))

def copy_global_configuration(src, dest):
    setattr(dest, 'output_dir', src.output_dir)
    setattr(dest, 'processes', src.processes)
    setattr(dest, 'threads', src.threads)
    setattr(dest, 'main_log', src.main_log)

def setup_whole_configuration(args, func, temp_output_files):
    setattr(args, 'readsqc_dir', os.path.join(args.output_dir, 'readsqc'))
    setattr(args, 'assemble_dir', os.path.join(args.output_dir, 'assemble'))
    setattr(args, 'filter_dir', os.path.join(args.output_dir, 'filter'))
    setattr(args, 'orf_predict_dir', os.path.join(args.output_dir, 'orf_prediction'))
    setattr(args, 'annotate_dir', os.path.join(args.output_dir, 'annotation'))
    setattr(args, 'quantify_dir', os.path.join(args.output_dir, 'quantify'))
    setattr(args, 'report_dir', os.path.join(args.output_dir, 'report'))

    if len(list(args.input)) > 0:
        args.host = list(args.host)
        args.input = list(args.input)
        args.input.sort()


        setattr(args, 'raw_input1', args.input[0])
        setattr(args, 'raw_input2', args.input[1])
        setattr(args, 'input1', args.raw_input1)
        setattr(args, 'input2', args.raw_input2)
        #if not (hasattr(args, 'input1') and hasattr(args, 'input2')):
        if func == 'readsqc':
            args.input1 = get_reformatted_identifiers(args.raw_input1, 1, args.output_dir, temp_output_files)
            args.input2 = get_reformatted_identifiers(args.raw_input2, 2, args.output_dir, temp_output_files)
        
        if len(args.host) > 0:
            setattr(args, 'input1_trimmed', os.path.join(args.readsqc_dir, 'kneaddata_paired_1.fastq'))
            setattr(args, 'input2_trimmed', os.path.join(args.readsqc_dir, 'kneaddata_paired_2.fastq'))
        else:
            setattr(args, 'input1_trimmed', os.path.join(args.readsqc_dir, 'kneaddata.trimmed.1.fastq'))
            setattr(args, 'input2_trimmed', os.path.join(args.readsqc_dir, 'kneaddata.trimmed.2.fastq'))

    #assemble model configuration
    setattr(args, 'contigs', os.path.join(args.assemble_dir, 'final_assembly.fasta') if not args.input_contigs else args.input_contigs)
    setattr(args, 'contigs_filtered', os.path.join(args.filter_dir, 'final_assembly_filtered.fasta'))

    #Orf predict model configuration 
    setattr(args, 'predict_aa', os.path.join(args.orf_predict_dir, 'predict_prot.faa'))
    setattr(args, 'predict_nuc', os.path.join(args.orf_predict_dir, 'predict_nucl.fasta'))
    setattr(args, 'predict_gff', os.path.join(args.orf_predict_dir, 'predict.gff'))
    
    setattr(args, 'predict_aa_filtered', os.path.join(args.filter_dir, 'predict_aa_filtered.fasta'))
    setattr(args, 'predict_nuc_filtered', os.path.join(args.filter_dir, 'predict_nuc_filtered.fasta'))

    #annotate model configuration
    setattr(args, 'virus_anno', os.path.join(args.annotate_dir, 'virus_annotation.txt'))
    setattr(args, 'nonvirus_anno', os.path.join(args.annotate_dir, 'nonvirus_annotation.txt'))
    
    #quantify model configuration
    #setattr(args, 'reference', )

    #report model configuration
    setattr(args, 'quant', os.path.join(args.quantify_dir, 'quant.sf'))
    setattr(args, 'cluster_file', os.path.join(args.filter_dir, 'predict_aa_filtered.fasta.clstr') if args.blast_type=='blastp' else os.path.join(args.filter_dir, 'predict_nuc_filtered.fasta.clstr'))

    if func == 'readsqc':
        create_directory(args.readsqc_dir)
        readsqc_args = argparse.Namespace()
        copy_global_configuration(args, readsqc_args)
        setattr(readsqc_args, 'readsqc_dir', args.readsqc_dir)
        setattr(readsqc_args, 'input1', args.input1)
        setattr(readsqc_args, 'input2', args.input2)
        setattr(readsqc_args, 'host', args.host)
        setattr(readsqc_args, 'readsqc_log', args.readsqc_log)
        readsqc_args.memory = args.raw_memory * 1000
        readsqc_args.memory = str(readsqc_args.memory) + 'm'

        readsqc_args.readsqc_exe = find_dependency(
            config.kneaddata_path,
            config.kneaddata_exe,
            'kneaddata'
        )
        return readsqc_args

    if func == 'assemble':
        create_directory(args.assemble_dir)
        assemble_args = argparse.Namespace()
        copy_global_configuration(args, assemble_args)
        setattr(assemble_args, 'assemble_dir', args.assemble_dir)
        setattr(assemble_args, 'input1', args.input1_trimmed if os.path.exists(args.input1_trimmed) else args.input1)
        setattr(assemble_args, 'input2', args.input2_trimmed if os.path.exists(args.input2_trimmed) else args.input2)
        setattr(assemble_args, 'assemble_log', args.assemble_log)
        setattr(assemble_args, 'assembler', args.assembler)
        if assemble_args.assembler == 'megahit':
            assemble_args.memory = str(args.raw_memory * 1000000000)
            assemble_args.assemble_exe = find_dependency(
                config.megahit_path,
                config.megahit_exe,
                'megahit'
            )
        elif assemble_args.assembler == 'metaspades':
            assemble_args.memory = str(args.raw_memory)
            assemble_args.assemble_exe = find_dependency(
                config.metaspades_path,
                config.metaspades_exe,
                'metaspades'
            )
        return assemble_args

    if func == 'filter':
        create_directory(args.filter_dir)
        filter_args = argparse.Namespace()
        copy_global_configuration(args, filter_args)
        setattr(filter_args, 'filter_dir', args.filter_dir)
        setattr(filter_args, 'is_contig_filter', args.is_contig_filter)
        setattr(filter_args, 'reformat_out', os.path.join(args.filter_dir, 'reformat.fasta'))
        setattr(filter_args, 'filter_log', args.assemble_filter_log if args.is_contig_filter else args.filter_log)
        setattr(filter_args, 'min_len', args.min_contig_len if args.is_contig_filter else args.min_len)
        setattr(filter_args, 'max_len', args.max_contig_len if args.is_contig_filter else args.max_len)
        setattr(filter_args, 'min_id', args.min_contig_id if args.is_contig_filter else args.min_id)
        setattr(filter_args, 'min_coverage', args.min_contig_coverage if args.is_contig_filter else args.min_coverage)
        setattr(filter_args, 'memory', args.raw_memory)
        setattr(filter_args, 'seq_type', 'nucl' if args.is_contig_filter else args.seq_type)
        setattr(filter_args, 'nucl', args.contigs if args.is_contig_filter else args.predict_nuc)
        setattr(filter_args, 'prot', args.predict_aa)
        
        filter_args.reformat_exe = find_dependency(
            config.reformat_path,
            config.reformat_exe,
            'reformat'
        )
        if filter_args.seq_type == 'nucl':
            setattr(filter_args, 'filter_in', filter_args.nucl)
            setattr(filter_args, 'filter_out', os.path.join(filter_args.filter_dir, 'predict_nuc_filtered.fasta'))
            if not args.is_contig_filter:
                setattr(filter_args, 'filter_in_another', filter_args.prot)
                setattr(filter_args, 'filter_out_another', os.path.join(filter_args.filter_dir, 'predict_aa_filtered.fasta'))
            filter_args.cdhit_exe = find_dependency(
            config.cdhit_path,
            config.cdhitest_exe,
            'cd-hit-est'
            )
        elif filter_args.seq_type == 'prot':
            setattr(filter_args, 'filter_in', filter_args.prot)
            setattr(filter_args, 'filter_out', os.path.join(filter_args.filter_dir, 'predict_aa_filtered.fasta'))
            setattr(filter_args, 'filter_in_another', filter_args.nucl)
            setattr(filter_args, 'filter_out_another', os.path.join(filter_args.filter_dir, 'predict_nuc_filtered.fasta'))
            filter_args.cdhit_exe = find_dependency(
            config.cdhit_path,
            config.cdhit_exe,
            'cd-hit'
        )
        return filter_args

    if func == 'orf_predict':
        create_directory(args.orf_predict_dir)
        orf_predict_args = argparse.Namespace()
        copy_global_configuration(args, orf_predict_args)
        setattr(orf_predict_args, 'orf_predict_dir', args.orf_predict_dir)
        setattr(orf_predict_args, 'orf_predict_log', args.orf_predict_log)
        setattr(orf_predict_args, 'contigs', args.contigs_filtered if args.is_contig_filter else args.contigs)
        setattr(orf_predict_args, 'predict_aa', args.predict_aa)
        setattr(orf_predict_args, 'predict_nuc', args.predict_nuc)
        setattr(orf_predict_args, 'predict_gff', args.predict_gff)

        if os.path.exists(orf_predict_args.contigs):
            #decompress contigs file if required
            setattr(args, 'raw_contigs', orf_predict_args.contigs)
            orf_predict_args.contigs = decompress_file(orf_predict_args.contigs, args.output_dir, temp_output_files)
        else:
            logger.warning("Error: No input contigs! Cannot run Orf Predict Model!")
            sys.exit("Error: No input contigs! Cannot run Orf Predict Model!")

        orf_predict_args.predict_exe = find_dependency(
                config.prodigal_path,
                config.prodigal_exe,
                'prodigal'
            )
        return orf_predict_args
    
    if func == 'annotate':
        create_directory(args.annotate_dir)
        annotate_args = argparse.Namespace()
        copy_global_configuration(args, annotate_args)
        setattr(annotate_args, 'annotate_dir', args.annotate_dir)
        setattr(annotate_args, 'annotate_log', args.annotate_log)
        setattr(annotate_args, 'diamond', args.diamond)
        setattr(annotate_args, 'blast_type', args.blast_type)
        setattr(annotate_args, 'virus_anno', args.virus_anno)
        setattr(annotate_args, 'nonvirus_anno', args.nonvirus_anno)
        setattr(annotate_args, 'virus', args.virus)
        setattr(annotate_args, 'non_virus', args.non_virus)

        if os.path.exists(args.predict_aa_filtered) or os.path.exists(args.predict_nuc_filtered):
            setattr(annotate_args, 'query', args.predict_aa_filtered if annotate_args.blast_type == 'blastp' else args.predict_nuc_filtered)
        else:
            setattr(annotate_args, 'query', args.predict_aa if annotate_args.blast_type == 'blastp' else args.predict_nuc)

        if annotate_args.diamond:
            annotate_args.annotate_exe = find_dependency(
                config.diamond_path,
                config.diamond_exe,
                'diamond'
            )
        elif annotate_args.blast_type == 'blastx':
            annotate_args.annotate_exe = find_dependency(
                config.blast_path,
                config.blastx_exe,
                'blastx'
            )
        elif annotate_args.blast_type == 'blastp':
            annotate_args.annotate_exe = find_dependency(
                config.blast_path,
                config.blastp_exe,
                'blastp'
            )
        return annotate_args

    if func == 'quantify':
        create_directory(args.quantify_dir)
        quantify_args = argparse.Namespace()
        copy_global_configuration(args, quantify_args)
        setattr(quantify_args, 'quantify_dir', args.quantify_dir)
        setattr(quantify_args, 'quantify_log', args.quantify_log)
        setattr(quantify_args, 'quant_index', os.path.join(quantify_args.quantify_dir, 'quant_index'))
        setattr(quantify_args, 'input1', args.input1_trimmed if os.path.exists(args.input1_trimmed) else args.input1)
        setattr(quantify_args, 'input2', args.input2_trimmed if os.path.exists(args.input2_trimmed) else args.input2)
        setattr(quantify_args, 'reference', args.predict_nuc_filtered if os.path.exists(args.predict_nuc_filtered) else args.predict_nuc)

        quantify_args.quant_exe = find_dependency(
            config.salmon_path,
            config.salmon_exe,
            'salmon'
        )

        return quantify_args

    if func == 'report':
        create_directory(args.report_dir)
        report_args = argparse.Namespace()
        copy_global_configuration(args, report_args)
        setattr(report_args, 'report_dir', args.report_dir)
        setattr(report_args, 'report_log', args.report_log)
        setattr(report_args, 'virus_anno', args.virus_anno)
        setattr(report_args, 'nonvirus_anno', args.nonvirus_anno)
        setattr(report_args, 'quant', args.quant if os.path.exists(args.quant) else None)
        setattr(report_args, 'cluster_file', args.cluster_file)
        setattr(report_args, 'cluster_rep', args.cluster_rep if os.path.exists(args.cluster_file) else False)
        setattr(report_args, 'orf', args.predict_aa_filtered if os.path.exists(args.predict_aa_filtered) else args.predict_aa)
        setattr(report_args, 'contigs', args.contigs_filtered if os.path.exists(args.contigs_filtered) else args.contigs)
        setattr(report_args, 'one_minus_r', (100 - args.ratio) / 100)
        print(report_args)
        return report_args



def setup_separated_configuration(args, func, temp_output_files):
    if 'readsqc' in func:
        setattr(args, 'readsqc_dir', os.path.join(args.output_dir, 'readsqc'))
        create_directory(args.readsqc_dir)
        args.host = list(args.host)
        args.input = list(args.input)
        print(args.input)
        args.input.sort()
        print(args.input)
        args.memory = args.raw_memory * 1000
        args.memory = str(args.memory) + 'm'
        if len(args.input) == 2:
            setattr(args, 'input1', args.input[0])
            setattr(args, 'input2', args.input[1])
            setattr(args, 'raw_input1', args.input1)
            setattr(args, 'raw_input2', args.input2)
            args.input1 = get_reformatted_identifiers(args.input1, 1, args.output_dir, temp_output_files)
            args.input2 = get_reformatted_identifiers(args.input2, 2, args.output_dir, temp_output_files)
        else:
            sys.exit("Please provide two input sequence files.")

        args.readsqc_exe = find_dependency(
            config.kneaddata_path,
            config.kneaddata_exe,
            'kneaddata'
        )

    if 'assemble' in func:
        setattr(args, 'assemble_dir', os.path.join(args.output_dir, 'assemble'))
        create_directory(args.assemble_dir)
        args.input = list(args.input)
        print(args.input)
        args.input.sort()
        if len(args.input) == 2:
            setattr(args, 'input1', args.input[0])
            setattr(args, 'input2', args.input[1])
        else:
            sys.exit("Please provide two input sequence files.")

        if args.assembler == 'megahit':
            args.memory = str(args.raw_memory * 1000000000)
            args.assemble_exe = find_dependency(
                config.megahit_path,
                config.megahit_exe,
                'megahit'
            )
        elif args.assembler == 'metaspades':
            args.memory = str(args.raw_memory)
            args.assemble_exe = find_dependency(
                config.metaspades_path,
                config.metaspades_exe,
                'metaspades'
            )
        args.reformat_exe = find_dependency(
            config.reformat_path,
            config.reformat_exe,
            'reformat'
        )
        args.cdhit_exe = find_dependency(
            config.cdhit_path,
            config.cdhitest_exe,
            'cd-hit-est'
        )

    if 'filter' in func:
        setattr(args, 'filter_dir', os.path.join(args.output_dir, 'filter'))
        create_directory(args.filter_dir)
        setattr(args, 'reformat_out', os.path.join(args.filter_dir, 'reformat.fasta'))
        args.reformat_exe = find_dependency(
            config.reformat_path,
            config.reformat_exe,
            'reformat'
        )
        if args.seq_type == 'nucl':
            setattr(args, 'filter_in', args.nucl)
            setattr(args, 'filter_out', os.path.join(args.filter_dir, 'predict_nuc_filtered.fasta'))
            if 'prot' in args:
                setattr(args, 'filter_in_another', args.prot)
                setattr(args, 'filter_out_another', os.path.join(args.filter_dir, 'predict_aa_filtered.fasta'))
            args.cdhit_exe = find_dependency(
            config.cdhit_path,
            config.cdhitest_exe,
            'cd-hit-est'
            )
        elif args.seq_type == 'prot':
            setattr(args, 'filter_in', args.prot)
            setattr(args, 'filter_out', os.path.join(args.filter_dir, 'predict_aa_filtered.fasta'))
            if 'nucl' in args:
                setattr(args, 'filter_in_another', args.nucl)
                setattr(args, 'filter_out_another', os.path.join(args.filter_dir, 'predict_nuc_filtered.fasta'))
            args.cdhit_exe = find_dependency(
            config.cdhit_path,
            config.cdhit_exe,
            'cd-hit'
        )

    if 'orf_predict' in func:
        setattr(args, 'orf_predict_dir', os.path.join(args.output_dir, 'orf_prediction'))
        create_directory(args.orf_predict_dir)
        setattr(args, 'predict_aa', os.path.join(args.orf_predict_dir, 'predict_prot.faa'))
        setattr(args, 'predict_nuc', os.path.join(args.orf_predict_dir, 'predict_nucl.fasta'))
        setattr(args, 'predict_gff', os.path.join(args.orf_predict_dir, 'predict.gff'))
        if args.contigs != None:
            #decompress contigs file if required
            setattr(args, 'raw_contigs', args.contigs)
            args.contigs = decompress_file(args.contigs, args.output_dir, temp_output_files)

        args.predict_exe = find_dependency(
                config.prodigal_path,
                config.prodigal_exe,
                'prodigal'
            )
    
    if 'annotate' in func:
        setattr(args, 'annotate_dir', os.path.join(args.output_dir, 'annotation'))
        create_directory(args.annotate_dir)
        setattr(args, 'virus_anno', os.path.join(args.annotate_dir, 'virus_annotation.txt'))
        setattr(args, 'nonvirus_anno', os.path.join(args.annotate_dir, 'nonvirus_annotation.txt'))
        if args.diamond:
            args.annotate_exe = find_dependency(
                config.diamond_path,
                config.diamond_exe,
                'diamond'
            )
        elif args.blast_type == 'blastx':
            args.annotate_exe = find_dependency(
                config.blast_path,
                config.blastx_exe,
                'blastx'
            )
        elif args.blast_type == 'blastp':
            args.annotate_exe = find_dependency(
                config.blast_path,
                config.blastp_exe,
                'blastp'
            )

    if 'quantify' in func:
        setattr(args, 'quantify_dir', os.path.join(args.output_dir, 'quantify'))
        create_directory(args.quantify_dir)
        setattr(args, 'quant_index', os.path.join(args.quantify_dir, 'quant_index'))

        args.quant_exe = find_dependency(
            config.salmon_path,
            config.salmon_exe,
            'salmon'
        )

    if 'report' in func:
        setattr(args, 'report_dir', os.path.join(args.output_dir, 'report'))
        create_directory(args.report_dir)
        setattr(args, 'one_minus_r', (100 - args.ratio) / 100)


def update_configuration(args, func, temp_output_files, run_type):
    if run_type == 'whole':
        return setup_whole_configuration(args, func, temp_output_files)
    elif run_type == 'separated':
        setup_separated_configuration(args, func, temp_output_files)