#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import pandas as pd
from cyvcf2 import VCF
from tqdm import tqdm

VCF_FILE = "../input/exoma.vcf.gz"
OUTPUT = "../output/01_Variantes_VEP.xlsx"

print("="*70)
print("EXOMA EXPLORER V2")
print("ETAPA 1 - EXTRAÇÃO VEP")
print("="*70)
print()

vcf = VCF(VCF_FILE)

print("VCF carregado com sucesso.")

