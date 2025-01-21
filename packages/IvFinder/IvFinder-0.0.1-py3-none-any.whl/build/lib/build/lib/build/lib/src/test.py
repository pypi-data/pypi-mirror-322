from multiprocessing import cpu_count  # cpu核心数模块，其可以获取 CPU 核心数
import decimal

from Bio import SeqIO
from ete3 import NCBITaxa
from Bio import Entrez
import importlib_resources
import os
import sys
BASE_DIR=  os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))                   
# 将这个路径添加到环境变量中。
sys.path.append( BASE_DIR  )
Entrez.email = "yyf1970199923@mail.ustc.edu.cn"
Entrez.api_key = 'c2536734054268f84f60f6757cf76729a707'
ncbi = NCBITaxa()
acc2tax = dict()

print(ncbi.get_rank([10239]))

print(BASE_DIR)
my_resources = importlib_resources.files("data")
data = (my_resources / "data" / "TaxID.csv")

print(my_resources)
print(data)