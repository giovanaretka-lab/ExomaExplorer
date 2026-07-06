#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 4 - Painéis de Genes
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

OUTPUT = BASE / "output"
BANCOS = BASE / "bancos"

ARQUIVO = OUTPUT / "02_Base_Mestre.xlsx"
SAIDA = OUTPUT / "04_Paineis.xlsx"

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 4 - PAINÉIS")
print("=" * 70)
print()

print("Lendo Base Mestre...")

df = pd.read_excel(ARQUIVO)

print(f"Registros carregados: {len(df):,}")
print()
# =====================================================
# CARREGA PAINÉIS
# =====================================================

print("Procurando painéis de genes...")

paineis = {}

for arquivo in sorted(BANCOS.glob("*.txt")):

    nome = arquivo.stem

    with open(arquivo, "r", encoding="utf-8") as f:

        genes = {
            linha.strip().upper()
            for linha in f
            if linha.strip()
        }

    paineis[nome] = genes

print(f"Painéis encontrados: {len(paineis)}")

for nome in paineis:
    print(f" - {nome}: {len(paineis[nome])} genes")

print()
# =====================================================
# GERA RELATÓRIO DOS PAINÉIS
# =====================================================

print("Gerando painéis...")

with pd.ExcelWriter(
    SAIDA,
    engine="xlsxwriter"
) as writer:

    # Aba completa
    df.to_excel(
        writer,
        sheet_name="Todas",
        index=False
    )

    # Uma aba para cada painel
    for nome, genes in paineis.items():

        painel = df[
            df["SYMBOL"]
            .fillna("")
            .str.upper()
            .isin(genes)
        ]

        painel.to_excel(
            writer,
            sheet_name=nome[:31],
            index=False
        )

        print(
            f"{nome}: {len(painel):,} variantes"
        )

print()

print("=" * 70)
print("PAINÉIS GERADOS COM SUCESSO")
print("=" * 70)
print()

print(f"Arquivo: {SAIDA}")
