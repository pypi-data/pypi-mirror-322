import os
import sys
BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )

import re
import decimal
import math
import traceback
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from . import CAT_radical
import argparse
import openpyxl
import decimal
import math
from Bio import SeqIO
from ete3 import NCBITaxa
from Bio import Entrez


def get_percentage(readn_dict, sumreads):
    for key in readn_dict.keys():
        readn_dict[key]['percentage'] = (decimal.Decimal(readn_dict[key]['numreads']) / decimal.Decimal(sumreads)) * 100
        readn_dict[key]['percentage'] = round(readn_dict[key]['percentage'], 15)
    return readn_dict


def parse_tabular_alignment(alignment_file, one_minus_r):
    headers=['qseqid','sseqid','bitscore','evalue','pident','length','stitle']
    tabular_alignment = pd.read_csv(alignment_file, sep='\t', header=None, names=headers, dtype={'bitscore': str, 'pident':str})
    ORF2hits = dict()
    ORF_done = False
    taxid_done = []
    for i in range(len(tabular_alignment)):
        ORF = tabular_alignment.loc[i, 'qseqid']
        hit = tabular_alignment.loc[i, 'sseqid']
        taxid = hit.split('|')[-1]
        if ORF in ORF2hits.keys():
            if taxid in taxid_done or ORF_done == True:
                continue

        #hit = tabular_alignment.loc[i, 'sseqid']
        ident = decimal.Decimal(tabular_alignment.loc[i, 'pident'])
        product = tabular_alignment.loc[i, 'stitle']

        #print(tabular_alignment.loc[i, 'bitscore'])
        bitscore = decimal.Decimal(tabular_alignment.loc[i, 'bitscore'])

        if ORF not in ORF2hits.keys():
            #reach a new ORF
            ORF2hits[ORF] = {'hits_list':[], 'top_bitscore': bitscore}
            top_bitscore = bitscore
            ORF_done = False
            taxid_done = []
            #ORF2hits[ORF].append((hit, ident, product, bitscore))

        if bitscore >= one_minus_r * top_bitscore:
            ORF2hits[ORF]['hits_list'].append((hit, ident, product, bitscore, taxid))
            taxid_done.append(taxid)
            if bitscore > top_bitscore:
                ORF2hits[ORF]['top_bitscore'] = bitscore
        else:
            ORF_done = True
    #print(ORF2hits)
    return ORF2hits

def parse_faa(ORF_faa):
    contig2ORFs = dict()
    protein_parse = SeqIO.parse(ORF_faa, 'fasta')
    for protein_record in protein_parse:
        ORF = protein_record.id
        contig = ORF.rsplit("_", 1)[0]

        if contig not in contig2ORFs.keys():
            contig2ORFs[contig] = []

        contig2ORFs[contig].append(ORF)

    return contig2ORFs

def parse_abundance_file(ORF_abundance):
    contig2reads = dict()
    for i in range(len(ORF_abundance)):
        ORF = ORF_abundance.loc[i, 'Name']
        tpm = ORF_abundance.loc[i, 'TPM']
        numreads = ORF_abundance.loc[i, 'NumReads']
        contig = ORF.rsplit("_", 1)[0]
        if contig not in contig2reads.keys():
            contig2reads[contig] = []

        contig2reads[contig].append((ORF, tpm, numreads))

    return contig2reads

def parse_cluster_file(cluster_file):
    open_file = open(cluster_file, 'r')
    cluster_rep_info = dict()
    cluster = []
    cluster_seed = ""
    for line in open_file.readlines():
        line = line.strip()
        if not len(line):
            continue
        
        if re.search('^>', line):       #new cluster
            for member in cluster:
                cluster_rep_info[member] = cluster_seed
            cluster = []
            continue

        mym = re.search('>(.+)\.{3}', line)
        myid = mym.group(1)
        if re.search('\*$', line):
            cluster_seed = myid
        else:
            cluster.append(myid)

    return cluster_rep_info

def merge_dict(dict1, dict2):
    if dict2:
        for key, value in dict2.items():
            if key not in dict1.keys():
                dict1[key] = decimal.Decimal('0.0')
            dict1[key] += value

def get_LCAs_ORFs(contig_name, hits):
    virus2tax = dict()
    ORF2tax = dict()
    virus2multitax = dict()
    virus_tax2score = dict()
    nonvirus_tax2score = dict()
    based_on_n_ORFs = 0
    sum_virus_score = decimal.Decimal('0.0')
    sum_nonvirus_score = decimal.Decimal('0.0')
    sum_virus_identity = decimal.Decimal('0.0')
    for (ORF_name, virus_hit, nonvirus_hit) in hits:
        nonvirus_top_bitscore = decimal.Decimal('0.0')
        nonvirus_top_identity = decimal.Decimal('0.0')
        virus_top_bitscore = decimal.Decimal('0.0')
        virus_top_identity = decimal.Decimal('0.0')

        if nonvirus_hit:
            (nonvirus_top_bitscore, nonvirus_top_identity, _) = CAT_radical.find_LCA_for_ORF(nonvirus_hit)

        if virus_hit:
            (virus_top_bitscore, virus_top_identity, temp_tax2score) = CAT_radical.find_LCA_for_ORF(virus_hit)
            #print(temp_tax2score)
            if virus_top_bitscore > nonvirus_top_bitscore or virus_top_identity >= 85.0:
                merge_dict(virus_tax2score, temp_tax2score)
                based_on_n_ORFs += 1
        
        if contig_name == 'k141_54967':
            print(virus_hit)
            print(temp_tax2score)
        sum_virus_score += virus_top_bitscore
        sum_nonvirus_score += nonvirus_top_bitscore
    #print(contig_name,sum_virus_score, sum_nonvirus_score)
    if not virus_tax2score or sum_virus_score < sum_nonvirus_score * decimal.Decimal('0.9'):
        #print('{0}\tno virus taxid assigned\t'
                    #'no virus hits to database\n'.format(contig_name))
        return virus2tax, None, ORF2tax, virus2multitax
    
    best_lineage, best_scores, best_lineages_scores = CAT_radical.find_weighted_LCA(virus_tax2score, 0.5)
    #print(best_lineage)
    scores = ['{0:.3f}'.format(score) for
            score in best_scores]
    virus2tax[contig_name] = {
        'contig': contig_name,
        'taxid': best_lineage[0],
        'classification': 'taxid assigned',
        'organism': CAT_radical.find_name(best_lineage[0]),
        'taxonomy': CAT_radical.find_tax(best_lineage[0]),
        'reason': 'based on {0}/{1} ORFs'.format(based_on_n_ORFs, len(hits)),
        'lineage': ';'.join(str(x) for x in best_lineage[::-1]),
        'lineage score': ';'.join(str(x) for x in scores[::-1]),
        'virus_score:nonvirus_score': str(sum_virus_score)+':'+str(sum_nonvirus_score)
    }
    num = 1
    for (lineage, lineage_scores) in best_lineages_scores:
        scores = ['{0:.3f}'.format(score) for
            score in lineage_scores]
        virus2multitax[contig_name +' tax'+str(num)] = {
            'contig': contig_name,
            'taxid': lineage[0],
            'classification': 'taxid assigned',
            'organism': CAT_radical.find_name(lineage[0]),
            'taxonomy': CAT_radical.find_tax(lineage[0]),
            'reason': 'based on {0}/{1} ORFs'.format(based_on_n_ORFs, len(hits)),
            'lineage': ';'.join(str(x) for x in lineage[::-1]),
            'lineage score': ';'.join(str(x) for x in scores[::-1]),
            'virus_score:nonvirus_score': str(sum_virus_score)+':'+str(sum_nonvirus_score)
        }
        num += 1

    if contig_name == 'k141_54967':
        print(virus_tax2score)
        print(best_lineages_scores)
        print(virus2multitax)
    num = 0
    for (ORF_name, virus_hit, nonvirus_hit) in hits:
        if virus_hit:
            ORF2tax[ORF_name] = virus_hit[0][2]
            temp_ident = virus_hit[0][1]
            for (hit, ident, product, bitscore, taxid) in virus_hit:
                if taxid == best_lineage[0]:
                    ORF2tax[ORF_name] = product
                    temp_ident = ident
            sum_virus_identity += temp_ident
            num += 1

    if sum_virus_score > sum_nonvirus_score * decimal.Decimal('0.9'):
        if sum_virus_score < sum_nonvirus_score * decimal.Decimal('1.1') or sum_virus_identity/num < 50.0:
            return None, virus2tax, ORF2tax, None
    
    return virus2tax, None, ORF2tax, virus2multitax

def classify_CAT(ORF_nonvirus, ORF_virus, contig2ORFs, cluster_rep_info, processes):
    virus2tax = dict()
    ORF2tax = dict()
    virus2multi_tax = dict()
    ambiguous_tax = dict()
    future_list = []

    pool = ProcessPoolExecutor(max_workers=processes)
    for contig in sorted(contig2ORFs):
        hits = []
        for ORF in contig2ORFs[contig]:
            #if ORF not in ORF_virus.keys() and ORF not in ORF_nonvirus.keys():
            #    continue
            
            if ORF in ORF_virus.keys():
                virus_hit = ORF_virus[ORF]['hits_list']
                virus_top_bitscore = ORF_virus[ORF]['top_bitscore']
            elif cluster_rep_info and ORF in cluster_rep_info.keys():
                cluster_rep = cluster_rep_info[ORF]
                if cluster_rep in ORF_virus.keys():
                    virus_hit = ORF_virus[cluster_rep]['hits_list']
                    virus_top_bitscore = ORF_virus[cluster_rep]['top_bitscore']
                else:
                    virus_hit = None
                    virus_top_bitscore = decimal.Decimal('0.0')
            else:
                virus_hit = None
                virus_top_bitscore = decimal.Decimal('0.0')

            if ORF in ORF_nonvirus.keys():
                nonvirus_hit = ORF_nonvirus[ORF]['hits_list']
                nonvirus_top_bitscore = ORF_nonvirus[ORF]['top_bitscore']
            elif cluster_rep_info and ORF in cluster_rep_info.keys():
                cluster_rep = cluster_rep_info[ORF]
                if cluster_rep in ORF_nonvirus.keys():
                    nonvirus_hit = ORF_nonvirus[cluster_rep]['hits_list']
                    nonvirus_top_bitscore = ORF_nonvirus[cluster_rep]['top_bitscore']
                else:
                    nonvirus_hit = None
                    nonvirus_top_bitscore = decimal.Decimal('0.0')
            else:
                nonvirus_hit = None
                nonvirus_top_bitscore = decimal.Decimal('0.0')
            
            #if virus_top_bitscore > nonvirus_top_bitscore:
            hits.append((ORF, virus_hit, nonvirus_hit))
        #print(len(hits))
        future = pool.submit(get_LCAs_ORFs, contig, hits)
        future_list.append(future)
        #print(contig, future)
        
    for future in as_completed(future_list):
        if not future.cancelled():
            try: 
                tmp_virus2tax, tmp_ambiguous_tax, tmp_ORF2tax, tmp_virus2multi_tax = future.result()
                if tmp_virus2tax:
                    virus2tax.update(tmp_virus2tax)
                if tmp_ambiguous_tax:
                    ambiguous_tax.update(tmp_ambiguous_tax)
                if tmp_virus2multi_tax:
                    virus2multi_tax.update(tmp_virus2multi_tax)
                ORF2tax.update(tmp_ORF2tax)
            except Exception as e:
                for future in future_list:
                    future.cancel()
                #event.set()
                pool.shutdown(wait=True)
                raise Exception(e)
        #else:
            #print("Cancelled")
    pool.shutdown()
    return virus2tax, ambiguous_tax, ORF2tax, virus2multi_tax

def abundance_caculate(virus2tax, ORF2tax, contig2reads):
    virus2readn = dict()
    organism2readn = dict()
    virus_sumreads = 0.0
    organism_sumreads = 0.0
    for contig in sorted(virus2tax):
        if contig not in contig2reads.keys():
            continue
        
        taxid = virus2tax[contig]['taxid']
        if taxid not in virus2readn.keys():
            virus2readn[taxid] = dict()
            virus2readn[taxid]['taxid'] = taxid
            virus2readn[taxid]['organism'] = virus2tax[contig]['organism']
            virus2readn[taxid]['taxonomy'] = virus2tax[contig]['taxonomy']
            virus2readn[taxid]['tpm'] = 0.0
            virus2readn[taxid]['numreads'] = 0.0

        for (ORF, tpm, numreads) in contig2reads[contig]: 
            
            if ORF not in ORF2tax.keys():
                continue
            virus2readn[taxid]['tpm'] += tpm
            virus2readn[taxid]['numreads'] += numreads
            virus_sumreads += numreads

            organism = ORF2tax[ORF]
            if organism not in organism2readn.keys():
                organism2readn[organism] = dict()
                organism2readn[organism]['taxonomy'] = organism
                organism2readn[organism]['tpm'] = 0.0
                organism2readn[organism]['numreads'] = 0.0
            
            organism2readn[organism]['tpm'] += tpm
            organism2readn[organism]['numreads'] = numreads
            organism_sumreads += numreads
    
    #del small abundance virus
    virus_to_del = [key for key in virus2readn if virus2readn[key]['numreads'] < 10]
    organism_to_del = [key for key in organism2readn if organism2readn[key]['numreads'] < 10]

    for key in virus_to_del:
        virus_sumreads -= virus2readn[key]['numreads']
        del virus2readn[key]

    for key in organism_to_del:
        organism_sumreads -= organism2readn[key]['numreads']
        del organism2readn[key]

    print('virus_sumreads:{0}\torganism_sumreads:{1}'.format(virus_sumreads, organism_sumreads))
    virus_abundance = get_percentage(virus2readn, virus_sumreads)
    organism_abundance = get_percentage(organism2readn, organism_sumreads)

    virus_abundance = dict(sorted(virus_abundance.items(), key=lambda x: x[1]['percentage'], reverse=True))
    organism_abundance = dict(sorted(organism_abundance.items(), key=lambda x: x[1]['percentage'], reverse=True))
    return virus_abundance, organism_abundance

def classify(virus_annotation, nonvirus_annotation, ORF_abundance, ORF_faa, cluster_rep, cluster_file, one_minus_r, processes):
    ORF_virus = parse_tabular_alignment(virus_annotation, one_minus_r)
    ORF_nonvirus = parse_tabular_alignment(nonvirus_annotation, one_minus_r)
    contig2ORFs = parse_faa(ORF_faa)
    if cluster_rep:
        cluster_rep_info = parse_cluster_file(cluster_file)
    else:
        cluster_rep_info = None

    virus2tax, ambiguous_tax, ORF2tax, virus2multi_tax = classify_CAT(ORF_nonvirus, ORF_virus, contig2ORFs, cluster_rep_info, processes)
    #print(virus2tax)

    if not ORF_abundance.empty:
        contig2reads = parse_abundance_file(ORF_abundance)
        virus_abundance, organism_abundance = abundance_caculate(virus2tax, ORF2tax, contig2reads)
    else:
        virus_abundance = None
        organism_abundance = None
    
    
    return virus2tax, ambiguous_tax, virus2multi_tax, virus_abundance, organism_abundance
