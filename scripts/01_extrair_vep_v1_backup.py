#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 1 - Extração das anotações VEP
"""

import gzip
from pathlib import Path

import pandas as pd
from cyvcf2 import VCF

# =====================================================
# CAMINHOS
# =====================================================

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "input"
OUTPUT = BASE / "output"

VCF_FILE = INPUT / "exoma.vcf.gz"
SAIDA = OUTPUT / "01_Variantes_VEP.xlsx"

# =====================================================
# INÍCIO
# =====================================================

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 1 - EXTRAÇÃO VEP")
print("=" * 70)
print()

if not VCF_FILE.exists():
    raise FileNotFoundError(f"VCF não encontrado:\n{VCF_FILE}")

print("Abrindo VCF...")

vcf = VCF(str(VCF_FILE))

# =====================================================
# LOCALIZA CABEÇALHO CSQ
# =====================================================

cabecalho = None

with gzip.open(VCF_FILE, "rt") as f:
    for linha in f:
        if linha.startswith("##INFO=<ID=CSQ"):
            cabecalho = linha.strip()
            break

if cabecalho is None:
    raise Exception("Campo CSQ não encontrado no VCF.")

descricao = cabecalho.split("Format: ")[1].split('">')[0]
campos = descricao.split("|")

print(f"Campos VEP encontrados: {len(campos)}")
print()

linhas = []

print("Extraindo variantes...")
print()
# =====================================================
# PERCORRE TODAS AS VARIANTES
# =====================================================

for variante in vcf:

    csq = variante.INFO.get("CSQ")

    if not csq:
        continue

    chrom = variante.CHROM
    pos = variante.POS
    ref = variante.REF
    alt = ",".join(variante.ALT)

    qual = variante.QUAL

    filtro = variante.FILTER
    if filtro is None:
        filtro = "PASS"

    for anotacao in csq.split(","):

        valores = anotacao.split("|")

        while len(valores) < len(campos):
            valores.append("")

        registro = dict(zip(campos, valores))
if registro.get("SYMBOL") == "NOD2":
    print("\n==============================")
    print("GENE:", registro.get("SYMBOL"))
    print("HGVSc:", registro.get("HGVSc"))
    print("HGVSp:", registro.get("HGVSp"))
    print("Protein_position:", registro.get("Protein_position"))
    print("Amino_acids:", registro.get("Amino_acids"))
    print("Codons:", registro.get("Codons"))
    print("Existing_variation:", registro.get("Existing_variation"))
    print("SIFT:", registro.get("SIFT"))
    print("PolyPhen:", registro.get("PolyPhen"))
    print("==============================")
    break
linhas.append({
            "CHROM": chrom,
            "POS": pos,
            "REF": ref,
            "ALT": alt,
            "QUAL": qual,
            "FILTER": filtro,

            "GENE": registro.get("SYMBOL", ""),
            "GENE_ID": registro.get("Gene", ""),
            "TRANSCRIPT": registro.get("Feature", ""),

            "HGVS_C": registro.get("HGVSc", ""),
            "HGVS_P": registro.get("HGVSp", ""),

            "CONSEQUENCE": registro.get("Consequence", ""),
            "IMPACT": registro.get("IMPACT", ""),

            "CLIN_SIG": registro.get("CLIN_SIG", ""),
            "PUBMED": registro.get("PUBMED", ""),

            "GNOMAD_AF": (
                registro.get("gnomADg_AF", "")
                or registro.get("gnomADe_AF", "")
            ),
        })
# =====================================================
# GERA PLANILHA
# =====================================================

print(f"Total de registros extraídos: {len(linhas)}")

df = pd.DataFrame(linhas)

OUTPUT.mkdir(exist_ok=True)

df.to_excel(
    SAIDA,
    index=False,
    engine="xlsxwriter"
)

print()
print("=" * 70)
print("EXTRAÇÃO CONCLUÍDA")
print("=" * 70)
print(f"Arquivo: {SAIDA}")
print(f"Registros: {len(df)}")
