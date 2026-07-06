#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import pandas as pd
from cyvcf2 import VCF

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 1 - EXTRAÇÃO VEP")
print("=" * 70)
print()

VCF_ARQUIVO = "../input/exoma.vcf.gz"
SAIDA = "../output/01_Variantes_VEP.xlsx"

print("Abrindo VCF...")
vcf = VCF(VCF_ARQUIVO)

# Localiza automaticamente o cabeçalho do campo CSQ
csq_header = None

for linha in vcf.raw_header.split("\n"):
    if linha.startswith("##INFO=<ID=CSQ"):
        csq_header = linha
        break

if csq_header is None:
    raise Exception("Campo CSQ não encontrado no VCF.")

descricao = csq_header.split("Format: ")[1].split('">')[0]
campos = descricao.split("|")

print(f"Campos VEP encontrados: {len(campos)}")
print()

# Lista que armazenará todas as variantes
linhas = []

print("Extraindo variantes...")

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

    csq = variante.INFO.get("CSQ")

    for anotacao in csq.split(","):

        valores = anotacao.split("|")

        while len(valores) < len(campos):
            valores.append("")

        registro = dict(zip(campos, valores))
        print(registro.get("SYMBOL"), registro.get("HGVSp"))
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

            "GNOMAD_AF": registro.get("gnomADg_AF", "") or registro.get("gnomADe_AF", "")
        })

print()
print(f"Total de registros extraídos: {len(linhas)}")

df = pd.DataFrame(linhas)

print("Salvando planilha...")

df.to_excel(
    SAIDA,
    index=False,
    engine="xlsxwriter"
)

print()
print("=" * 70)
print("EXTRAÇÃO CONCLUÍDA COM SUCESSO")
print("=" * 70)
print(f"Arquivo gerado: {SAIDA}")
print(f"Total de linhas: {len(df)}")

