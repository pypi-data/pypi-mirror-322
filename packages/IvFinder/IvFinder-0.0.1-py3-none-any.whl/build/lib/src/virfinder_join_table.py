import os
import sys
import multiprocessing
import traceback
import time
from run_module import *
from configs import options

import logging
import click
from ete3 import NCBITaxa
ncbi = NCBITaxa()
def find_tax(taxid):
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    tax_list = []
    for tax_id in lineage:
        tax_list.append(names[tax_id])
    return ';'.join(i for i in tax_list)

@click.command()
@click.option(
    '-i','--input',
    required=True,
    type=str
)
@click.option(
    '-o', '--output',
    required=True,
    type=str
)
def merge(input, output):
    print(input)
    root_path = os.path.abspath(input)
    print(root_path)
    sample_list = []
    for name in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, name)):
            virus_abundance_path = os.path.join(root_path, name, 'report/all_virus/virus_abundance.txt')
            if os.path.exists(virus_abundance_path):
                sample_list.append(name)
    print(sample_list)
    
    clade_list = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    clade2rank = {'superkingdom':0, 'kingdom':1, 'phylum':2, 'class':3, 'order':4, 'family':5, 'genus':6, 'species':7}
    output_file = pd.DataFrame(columns=['Clade', 'TaxID', 'Rank']+sample_list)
    num = 0
    for sample in sample_list:
        virus_abundance_path = os.path.join(root_path, sample, 'report/all_virus/virus_abundance.txt')
        virus_abundance = pd.read_csv(virus_abundance_path, sep='\t')
        virus_abundance.columns = ['TaxID', 'Virus Name', 'Lineage', 'TPM', 'NumReads', 'Percentage', 'Molecule Type']
        print(virus_abundance)
        for i in range(len(virus_abundance)):
            taxid = virus_abundance.loc[i, 'TaxID']
            lineages = ncbi.get_lineage(taxid)
            rank_list = ncbi.get_rank(lineages)
            for lineage in lineages:
                if rank_list[lineage] in clade_list:
                    if lineage in output_file.index:
                        if not pd.isna(output_file.loc[lineage, sample]):
                            output_file.loc[lineage, sample] += virus_abundance.loc[i, 'Percentage']
                        else:
                            output_file.loc[lineage, sample] = virus_abundance.loc[i, 'Percentage']
                    else:
                        output_file.loc[lineage, 'Clade'] = find_tax(lineage)
                        output_file.loc[lineage, 'TaxID'] = lineage
                        output_file.loc[lineage, 'Rank'] = clade2rank[rank_list[lineage]]
                        output_file.loc[lineage, sample] = virus_abundance.loc[i, 'Percentage']
        num += 1
        #if num ==2:
            #break
    print(output_file)
    output_file.sort_values(by=['Rank'], ascending=True, inplace=True)
    output_file.fillna(value=0, inplace=True)
    print(output_file)
    output_file.to_csv(output, sep='\t')

if __name__ == '__main__':
    merge()