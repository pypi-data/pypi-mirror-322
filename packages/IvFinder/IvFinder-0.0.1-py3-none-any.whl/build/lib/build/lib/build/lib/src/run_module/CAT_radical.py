import os
import sys
import numpy as np
import pandas as pd

import decimal
from ete3 import NCBITaxa
from Bio import Entrez
from Bio import SeqIO

Entrez.email = "yyf1970199923@mail.ustc.edu.cn"
Entrez.api_key = '650800723c67384cdceaccf335f236699208'
ncbi = NCBITaxa()
acc2tax = dict()
clade_list = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
clade2num = {'superkingdom':0, 'phylum':1, 'class':2, 'order':3, 'family':4, 'genus':5, 'species':6, 'no rank': -1}

def get_index(seq_id):
    seq_field = seq_id.split('|')
    if len(seq_field) == 1: #nonvirus result
        return seq_field[0], 'nonvirus', 2

    seq_db = seq_field[-2]
    seq_taxid = str(seq_field[-1])

    if seq_taxid == 'Unkown_taxid':     #Unkown Virus
        return seq_field[0], seq_db, 10239

    if seq_db == 'MGV':
        seq_index = seq_field[2]
    else:   #seq_db = RefSeq/GenBank/UniProt
        seq_index = seq_field[0]

    lineage = ncbi.get_lineage(seq_taxid)
    if 10239 not in lineage:
        print(seq_taxid)
        print(lineage)
        print('Not from Virus: ' + seq_id)

    return seq_index, seq_db, seq_taxid

def find_name(taxid):
    taxid = int(taxid)
    return ncbi.get_taxid_translator([taxid])[taxid]

def find_tax(taxid):
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    tax_list = []
    for tax_id in lineage:
        tax_list.append(names[tax_id])
    return ';'.join(i for i in tax_list)

def find_rank(taxid):
    rank_score = -1
    lineages = ncbi.get_lineage(taxid)
    rank_list = ncbi.get_rank(lineages)
    for lineage in lineages:
        rank = rank_list[lineage]
        if rank in clade2num.keys():
            score = clade2num[rank]
            if rank_score < score:
                rank_score = score
    return rank_score

def find_lineage(taxid):
    lineages = ncbi.get_lineage(taxid)
    lineages = list(reversed(lineages))
    return lineages

def find_LCA(list_of_lineages):
    overlap = set.intersection(*map(set, list_of_lineages))

    for taxid in list_of_lineages[0]:
        if taxid in overlap:
            return taxid
        
def find_LCA_for_ORF(hits):
    list_of_lineages = []
    tax2score = dict()
    top_bitscore = 0
    top_identity = 0
    top_organism = ''

    for (hit, ident, product, bitscore, taxid) in hits:
        seq_index, seq_db, seq_taxid = get_index(hit)
        if bitscore > top_bitscore:
            top_bitscore = bitscore
            top_identity = ident
            top_organism = find_name(seq_taxid) + ' [' + product + ']'
        
        lineage = find_lineage(seq_taxid)
        list_of_lineages.append(lineage)

        for taxid in lineage:
            if taxid not in tax2score.keys():
                tax2score[taxid] = bitscore
            else:
                if tax2score[taxid] < bitscore:
                    tax2score[taxid] = bitscore

    return top_bitscore, top_identity, tax2score

def find_weighted_LCA(tax2score, f):
    list_of_lineages = []
    list_of_bitscores = []
    based_on_n_ORFs = 0

    sum_bitscore = tax2score[1]

    whitelisted_lineages = []
    for taxid in tax2score.keys():
        if tax2score[taxid] / sum_bitscore > f:
            lineage = find_lineage(taxid)
            rank_score = find_rank(taxid)

            whitelisted_lineages.append((lineage, tax2score[taxid], rank_score))
    
    whitelisted_lineages = sorted(whitelisted_lineages,
        key=lambda x: x[2], reverse=True)
    #whitelisted_lineages = dict(sorted(whitelisted_lineages.items(), key=lambda x: x[1]['percentage'], reverse=True))
    #print(whitelisted_lineages)
    best_lineages = []
    best_lineages_scores = []

    best_lineage = []
    best_lineage_score = 0.0
    best_lineage_scores = []

    longest_length = 0
    highest_rank_score = -1
    
    taxid_trace = set()
    for (whitelisted_lineage, lineage_score, rank_score) in whitelisted_lineages:
        if whitelisted_lineage[0] not in taxid_trace:
            if highest_rank_score < rank_score:
                highest_rank_score = rank_score

            if highest_rank_score > rank_score:
                return best_lineage, best_lineage_scores, best_lineages_scores
            
            if best_lineage_score < lineage_score:
                best_lineage_score = lineage_score
                best_lineage = whitelisted_lineage
                best_lineage_scores = [tax2score[taxid] / sum_bitscore for
                    taxid in whitelisted_lineage]

            if lineage_score > best_lineage_score * decimal.Decimal('0.9'):
                best_lineages_scores.append((whitelisted_lineage, [tax2score[taxid] / sum_bitscore for
                    taxid in whitelisted_lineage]))

            taxid_trace |= set(whitelisted_lineage)
    return best_lineage, best_lineage_scores, best_lineages_scores