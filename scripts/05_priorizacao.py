#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 5 - Priorização Clínica
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

OUTPUT = BASE / "output"

ARQUIVO = OUTPUT / "03_Indice_Clinico.xlsx"
SAIDA = OUTPUT / "05_Priorizacao.xlsx"

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 5 - PRIORIZAÇÃO")
print("=" * 70)
print()

print("Lendo Índice Clínico...")

df = pd.read_excel(ARQUIVO)

print(f"Registros carregados: {len(df):,}")
print()
# =====================================================
# PRIORIZAÇÃO
# =====================================================

print("Criando listas prioritárias...")

top100 = df.sort_values(
    by="SCORE",
    ascending=False
).head(100)

patogenicas = df[
    df["IS_PATHOGENIC"] == True
]

likely = df[
    df["IS_LIKELY_PATHOGENIC"] == True
]

vus = df[
    df["IS_VUS"] == True
]

ultra = df[
    df["IS_ULTRA_RARA"] == True
]

novas = df[
    df["IS_NOVA"] == True
]

high = df[
    df["IS_HIGH"] == True
]

candidatas = df[
    (
        df["IS_ULTRA_RARA"]
        |
        df["IS_NOVA"]
    )
    &
    (
        df["IS_HIGH"]
        |
        df["IS_MODERATE"]
    )
]

print("Listas criadas.")
print()
# =====================================================
# SALVA RELATÓRIO
# =====================================================

print("Gerando relatório de priorização...")

with pd.ExcelWriter(
    SAIDA,
    engine="xlsxwriter"
) as writer:

    top100.to_excel(
        writer,
        sheet_name="Top100",
        index=False
    )

    patogenicas.to_excel(
        writer,
        sheet_name="Patogenicas",
        index=False
    )

    likely.to_excel(
        writer,
        sheet_name="Provavelmente_Pat",
        index=False
    )

    vus.to_excel(
        writer,
        sheet_name="VUS",
        index=False
    )

    ultra.to_excel(
        writer,
        sheet_name="Ultra_Raras",
        index=False
    )

    novas.to_excel(
        writer,
        sheet_name="Novas",
        index=False
    )

    high.to_excel(
        writer,
        sheet_name="HIGH",
        index=False
    )

    candidatas.to_excel(
        writer,
        sheet_name="Candidatas",
        index=False
    )

print()

print("=" * 70)
print("PRIORIZAÇÃO CONCLUÍDA")
print("=" * 70)
print()

print(f"Top100: {len(top100):,}")
print(f"Patogênicas: {len(patogenicas):,}")
print(f"Provavelmente Patogênicas: {len(likely):,}")
print(f"VUS: {len(vus):,}")
print(f"Ultra raras: {len(ultra):,}")
print(f"Novas: {len(novas):,}")
print(f"HIGH: {len(high):,}")
print(f"Candidatas: {len(candidatas):,}")

print()
print(f"Arquivo salvo em: {SAIDA}")
