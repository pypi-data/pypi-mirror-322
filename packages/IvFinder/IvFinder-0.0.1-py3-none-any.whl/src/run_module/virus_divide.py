import os
import sys
import decimal
import math
import traceback
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import importlib_resources
import argparse
import openpyxl
import decimal
import math
from Bio import SeqIO
from ete3 import NCBITaxa
from Bio import Entrez
ncbi = NCBITaxa()

def get_virus_type(virus2tax, virus_abundance):
    my_resources = importlib_resources.files("data")
    data = (my_resources / "taxid2virus.txt")
    #print(data)
    virus_type = pd.read_csv(data, sep='\t', index_col=0)
    #virus_type.set_index('taxid', inplace=True)
    dna_virus = {'tax':dict(), 'abundance':dict()}
    rna_virus = {'tax':dict(), 'abundance':dict()}
    unknown_virus = {'tax':dict(), 'abundance':dict()}

    for contig in virus2tax.keys():
        taxid = virus2tax[contig]['taxid']
        #molecule_type = 'unknown'
        if taxid not in virus_type.index:
            #print(taxid)
            new_taxid = taxid
            lineages = ncbi.get_lineage(taxid)
            lineages = list(reversed(lineages))
            for lineage in lineages:
                if lineage in virus_type.index:
                    new_taxid = lineage
                    break
                if lineage == 10239:
                    break
            if new_taxid != taxid:
                molecule_type = virus_type.loc[new_taxid, 'molecule type']
            else:
                molecule_type = 'unknown'
                #continue
        else:
            molecule_type = virus_type.loc[taxid, 'molecule type']

        virus2tax[contig]['molecule type'] = molecule_type
        if taxid in virus_abundance.keys():
            virus_abundance[taxid]['molecule type'] = molecule_type

            if 'DNA' in molecule_type:
                dna_virus['tax'][contig] = virus2tax[contig]
                dna_virus['abundance'][taxid] = virus_abundance[taxid]
            elif 'RNA' in molecule_type:
                rna_virus['tax'][contig] = virus2tax[contig]
                rna_virus['abundance'][taxid] = virus_abundance[taxid]
            else:
                unknown_virus['tax'][contig] = virus2tax[contig]
                unknown_virus['abundance'][taxid] = virus_abundance[taxid]

    return dna_virus, rna_virus, unknown_virus