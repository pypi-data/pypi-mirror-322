import os
from pydoc import describe
import sys
import shutil
from termios import VREPRINT
import csv
import re
import tarfile
import gzip

import collections
import multiprocessing
import argparse
import time
import glob
import datetime
from tkinter.messagebox import NO, RETRY

import pandas as pd
import numpy as np
import subprocess

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def parse_arguments(args):
    parser = argparse.ArgumentParser(usage='Install required database')
    parser.add_argument(
        '--kneaddata-database',
        choices=['human_genome','human_transcriptome', 'ribosomal_RNA', 'mouse_C57BL'],
        help='available kneaddata database'
    )
    parser.add_argument('-v', '--viral-seq', action='store', metavar='<filename>', help='Viral Seq Path')
    parser.add_argument('-b', '--bacteria-seq', action='store', metavar='<filename>', help='Bacteria Seq Path')
    parser.add_argument('-o', '--database-path', action='store', metavar='<directory>')
    parser.add_argument('-d', '--database-type', choices=['blast', 'diamond', 'all'], action='store', default='all', help='Database Type')
    parser.add_argument('-n', '--name', action='store', metavar='<filename>', help='the prefix of database')
    parser.add_argument('-t', '--threads', action ='store', metavar='<int>', type=int, default=1)
    return parser

def make_kneaddata_database(path):
    if args.kneaddata_database != None:
        command = 'kneaddata_database --download '
        command += args.kneaddata_database + ' bowtie2 ' + path
        print(command)
        ret = subprocess.run(command, shell=True)
        if ret.returncode == 0:
            print("Download kneaddata database successfully")
        else:
            print("Download kneaddata database failed")
    else:
        print("Skip download kneadddata database") 



def make_diamond_db(fasta_path, dbname, num_threads):
    make_diamond_command = 'diamond makedb -p ' + str(num_threads)
    make_diamond_command += ' --in ' + fasta_path + ' -d ' + dbname
    ret = subprocess.run(make_diamond_command, shell=True)
    if ret.returncode == 0:
        print("Make " + dbname + " Diamond DB complete!")
        return True
    else:
        print("Make " + dbname + " Diamond DB Error!")
        return False

def make_blast_db(fasta_path, dbname, dbtype):
    make_blast_command = 'makeblastdb -in ' + fasta_path
    make_blast_command += ' -out ' + dbname + ' -title ' + dbname
    make_blast_command += ' -dbtype ' + dbtype
    ret = subprocess.run(make_blast_command, shell=True)
    if ret.returncode == 0:
        print("Make " + dbname + " Blast DB complete!")
    else:
        print("Make " + dbname + " Blast DB Error!")

def make_viral_database(path, dbname, viral_seq, num_threads):
    blast_name = dbname + '.viral.blast'
    diamond_name = dbname + '.viral.diamond'
    if args.database_type == 'blast':
        make_blast_db(viral_seq, os.path.join(path, blast_name), 'prot')
    elif args.database_type == 'diamond':
        make_diamond_db(viral_seq, os.path.join(path, diamond_name), num_threads)
    elif args.database_type == 'all':
        make_blast_db(viral_seq, os.path.join(path, blast_name), 'prot')
        make_diamond_db(viral_seq, os.path.join(path, diamond_name), num_threads)

def make_bacteria_database(path, dbname, bacteria_seq, num_threads):
    blast_name = dbname + '.bacteria.blast'
    diamond_name = dbname + '.bacteria.diamond'
    if args.database_type == 'blast':
        make_blast_db(bacteria_seq, os.path.join(path, blast_name), 'prot')
    elif args.database_type == 'diamond':
        make_diamond_db(bacteria_seq, os.path.join(path, diamond_name), num_threads)
    elif args.database_type == 'all':
        make_blast_db(bacteria_seq, os.path.join(path, blast_name), 'prot')
        make_diamond_db(bacteria_seq, os.path.join(path, diamond_name), num_threads)

def make_dbs(args):
    kneaddata_path = os.path.join(args.database_path, 'kneaddata_database')
    make_kneaddata_database(kneaddata_path)

    if not os.path.exists(args.database_path):
        os.mkdir(args.database_path)

    if args.viral_seq:
        viral_folder = os.path.join(args.database_path, 'viral_database')
        if not os.path.exists(viral_folder):
            os.mkdir(viral_folder)
        make_viral_database(viral_folder, args.name, args.viral_seq, args.threads)
    if args.bacteria_seq:
        bacteria_folder = os.path.join(args.database_path, 'bacteria_database')
        if not os.path.exists(bacteria_folder):
            os.mkdir(bacteria_folder)
        make_bacteria_database(bacteria_folder, args.name, args.bacteria_seq, args.threads)

if __name__ == '__main__':
    parser = parse_arguments(sys.argv)
    args = parser.parse_args()
    print(args)
    make_dbs(args)