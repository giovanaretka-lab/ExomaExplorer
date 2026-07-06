#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 6 - Relatório Final
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

OUTPUT = BASE / "output"

ARQUIVO = OUTPUT / "05_Priorizacao.xlsx"
SAIDA = OUTPUT / "06_Relatorio_Final.xlsx"

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 6 - RELATÓRIO FINAL")
print("=" * 70)
print()

print("Lendo arquivo de priorização...")

xls = pd.ExcelFile(ARQUIVO)

print("Abas encontradas:")

for aba in xls.sheet_names:
    print(" -", aba)

print()
# =====================================================
# LÊ TODAS AS ABAS
# =====================================================

print("Carregando planilhas...")

abas = {}

for nome in xls.sheet_names:

    abas[nome] = pd.read_excel(
        ARQUIVO,
        sheet_name=nome
    )

print(f"{len(abas)} abas carregadas.")
print()

# =====================================================
# GERA RELATÓRIO
# =====================================================

print("Gerando relatório final...")

with pd.ExcelWriter(
    SAIDA,
    engine="xlsxwriter"
) as writer:

    # =================================================
    # RESUMO
    # =================================================

    resumo = pd.DataFrame({

        "Indicador":[
            "Top100",
            "Patogênicas",
            "Provavelmente Patogênicas",
            "VUS",
            "Ultra Raras",
            "Novas",
            "HIGH",
            "Candidatas"
        ],

        "Quantidade":[
            len(abas["Top100"]),
            len(abas["Patogenicas"]),
            len(abas["Provavelmente_Pat"]),
            len(abas["VUS"]),
            len(abas["Ultra_Raras"]),
            len(abas["Novas"]),
            len(abas["HIGH"]),
            len(abas["Candidatas"])
        ]

    })

    resumo.to_excel(
        writer,
        sheet_name="Resumo",
        index=False
    )

    # =================================================
    # COPIA TODAS AS ABAS
    # =================================================

    for nome, tabela in abas.items():

        tabela.to_excel(
            writer,
            sheet_name=nome[:31],
            index=False
        )

print()
print("=" * 70)
print("RELATÓRIO FINAL GERADO")
print("=" * 70)
print()
print(f"Arquivo: {SAIDA}")
