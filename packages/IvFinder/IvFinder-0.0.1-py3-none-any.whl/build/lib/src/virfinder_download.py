import os
import sys
import time
import argparse
import tarfile
from ete3 import NCBITaxa

from urllib.request import urlretrieve

download_link = "https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"

class DownloadReport():
    def __init__(self):
        self.start_time=time.time()

    def download_progress(self, block_num, block_size, total_size):
        """
        回调函数，用于显示下载进度
        """
        if block_num == 0:
            self.start_time = time.time()
            if total_size > 0:
                print("Downloading file of size: " + "{:.2f}".format(total_size / (1024.0**3)) + " GB\n")
        else:
            downloaded = block_num * block_size
            percent = (downloaded / total_size) * 100
            used_time = time.time()- self.start_time()
            rest_time = (total_size - downloaded) / (downloaded / used_time)
            rest_minutes = int(rest_time / 60)
            rest_seconds = rest_time - rest_minutes * 60
            info = '{:3.2f} % downloaded'.format(percent)
            print(info)

#urllib.request.urlretrieve(url, filename, download_progress)

ncbi = NCBITaxa()
ncbi.update_taxonomy_database('/data/users/yyf/databases/taxdump-2024.2.26.tar.gz')