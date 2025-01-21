import os
import sys
import decimal
import math
import traceback
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import decimal
import math
from Bio import SeqIO
from ete3 import NCBITaxa
from Bio import Entrez
ncbi = NCBITaxa()
import logging
import subprocess
logger=logging.getLogger(__name__)


def transfor_to_krona(virus_abundance, outdir):
    f = open(os.path.join(outdir, 'krona.txt'), 'w')
    for taxid in virus_abundance.keys():
        taxonomy = virus_abundance[taxid]['taxonomy']
        molecule_type = virus_abundance[taxid]['molecule type']
        percentage = virus_abundance[taxid]['percentage']
        
        if molecule_type != 'DNA' and 'DNA' in molecule_type:
            molecule_type = 'DNA\t' + molecule_type
        elif molecule_type != 'RNA' and 'RNA' in molecule_type:
            molecule_type = 'RNA\t' + molecule_type

        f.write(str(percentage))
        for taxon in taxonomy.split(';'):
            f.write('\t' + taxon)
            if taxon == 'Viruses':
                f.write('\t' + molecule_type)
        f.write('\n')

    f.close()
    return os.path.join(outdir, 'krona.txt')

def generate_krona(abundance_file, name, outdir, logger, report_log):
    krona_file = transfor_to_krona(abundance_file, outdir)
    krona_command = ['ktImportText']
    #krona_command += ['-t', str(col_taxid), '-m', str(col_score), krona_file]
    krona_command += [krona_file]
    krona_command += ['-o', os.path.join(outdir, name + '_krona.html')]
    exec_command = ' '.join(krona_command)
    logger.info("Command: " + exec_command)
    with open(report_log, 'a+') as logfile:
        subprocess.run(krona_command, shell=False, check=True,stderr=subprocess.STDOUT, stdout=logfile)
    
