#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 3 - Índice Clínico
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "output"
OUTPUT = BASE / "output"

ARQUIVO = INPUT / "02_Base_Mestre.xlsx"
SAIDA = OUTPUT / "03_Indice_Clinico.xlsx"

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 3 - ÍNDICE CLÍNICO")
print("=" * 70)
print()

print("Lendo Base Mestre...")

df = pd.read_excel(ARQUIVO)

print(f"Registros carregados: {len(df):,}")
print()
# =====================================================
# INDICADORES CLÍNICOS
# =====================================================

print("Criando indicadores clínicos...")

# Frequência
df["IS_NOVA"] = df["CATEGORIA_FREQ"] == "Nova"
df["IS_ULTRA_RARA"] = df["CATEGORIA_FREQ"] == "Ultra rara"
df["IS_MUITO_RARA"] = df["CATEGORIA_FREQ"] == "Muito rara"
df["IS_RARA"] = df["CATEGORIA_FREQ"] == "Rara"

# ClinVar
df["IS_PATHOGENIC"] = df["CLASSE_CLINVAR"] == "Patogênica"
df["IS_LIKELY_PATHOGENIC"] = (
    df["CLASSE_CLINVAR"] == "Provavelmente Patogênica"
)
df["IS_VUS"] = df["CLASSE_CLINVAR"] == "VUS"
df["IS_CONFLICTING"] = df["CLASSE_CLINVAR"] == "Conflitante"

# Impacto
df["IS_HIGH"] = df["IMPACT"] == "HIGH"
df["IS_MODERATE"] = df["IMPACT"] == "MODERATE"
df["IS_LOW"] = df["IMPACT"] == "LOW"

print("Indicadores criados.")
print()
# =====================================================
# PRIORIDADE CLÍNICA
# =====================================================

print("Calculando prioridade clínica...")

def prioridade(score):

    if score >= 18:
        return "Muito Alta"

    elif score >= 14:
        return "Alta"

    elif score >= 10:
        return "Moderada"

    elif score >= 6:
        return "Baixa"

    else:
        return "Muito Baixa"

df["PRIORIDADE"] = df["SCORE"].apply(prioridade)

print("Prioridade calculada.")
print()

# =====================================================
# RESUMO
# =====================================================

print("=" * 70)
print("RESUMO DO ÍNDICE CLÍNICO")
print("=" * 70)

print(df["PRIORIDADE"].value_counts())

print()
# =====================================================
# SALVA O ÍNDICE CLÍNICO
# =====================================================

print("Salvando Índice Clínico...")

df.to_excel(
    SAIDA,
    index=False,
    engine="xlsxwriter"
)

print()
print("=" * 70)
print("ÍNDICE CLÍNICO GERADO COM SUCESSO")
print("=" * 70)
print()
print(f"Arquivo: {SAIDA}")
