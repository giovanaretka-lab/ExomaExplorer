#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ExomaExplorer V2
ETAPA 2 - Base Mestre
"""

from pathlib import Path
import pandas as pd

# =====================================================
# CAMINHOS
# =====================================================

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "output"
OUTPUT = BASE / "output"

ARQUIVO_ENTRADA = INPUT / "01_Variantes_VEP.xlsx"
ARQUIVO_SAIDA = OUTPUT / "02_Base_Mestre.xlsx"

# =====================================================
# INÍCIO
# =====================================================

print("=" * 70)
print("EXOMA EXPLORER V2")
print("ETAPA 2 - BASE MESTRE")
print("=" * 70)
print()

if not ARQUIVO_ENTRADA.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado:\n{ARQUIVO_ENTRADA}"
    )

print("Lendo planilha...")

df = pd.read_excel(ARQUIVO_ENTRADA)

print(f"Registros carregados: {len(df):,}")

print()
# =====================================================
# PADRONIZAÇÃO DOS DADOS
# =====================================================

print("Padronizando dados...")

# Garante que a frequência seja numérica
df["GNOMAD_AF"] = pd.to_numeric(df["GNOMAD_AF"], errors="coerce").fillna(0)

# Remove espaços extras das colunas de texto
colunas_texto = [
    "GENE",
    "HGVS_C",
    "HGVS_P",
    "IMPACT",
    "CONSEQUENCE",
    "CLIN_SIG",
]

for coluna in colunas_texto:
    if coluna in df.columns:
        df[coluna] = (
            df[coluna]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# =====================================================
# CLASSIFICAÇÃO DA FREQUÊNCIA
# =====================================================

def classificar_frequencia(af):

    if af == 0:
        return "Nova"

    elif af < 0.0001:
        return "Ultra rara"

    elif af < 0.001:
        return "Muito rara"

    elif af < 0.01:
        return "Rara"

    else:
        return "Frequente"

df["CATEGORIA_FREQ"] = df["GNOMAD_AF"].apply(classificar_frequencia)

print("Classificação de frequência concluída.")
print()
# =====================================================
# CLASSIFICAÇÃO CLINVAR
# =====================================================

print("Classificando ClinVar...")

def classificar_clinvar(texto):

    texto = str(texto).lower()

    if "pathogenic" in texto and "likely" not in texto:
        return "Patogênica"

    elif "likely_pathogenic" in texto or "likely pathogenic" in texto:
        return "Provavelmente Patogênica"

    elif (
        "uncertain_significance" in texto
        or "uncertain significance" in texto
        or "vus" in texto
    ):
        return "VUS"

    elif "conflicting" in texto:
        return "Conflitante"

    elif "benign" in texto:
        return "Benigna"

    else:
        return ""

df["CLASSE_CLINVAR"] = df["CLIN_SIG"].apply(classificar_clinvar)

print("ClinVar classificado.")
print()

# =====================================================
# SCORE INICIAL
# =====================================================

print("Calculando Score...")

def calcular_score(linha):

    score = 0

    # Impacto
    if linha["IMPACT"] == "HIGH":
        score += 6

    elif linha["IMPACT"] == "MODERATE":
        score += 3

    # Frequência
    if linha["CATEGORIA_FREQ"] == "Nova":
        score += 6

    elif linha["CATEGORIA_FREQ"] == "Ultra rara":
        score += 5

    elif linha["CATEGORIA_FREQ"] == "Muito rara":
        score += 4

    elif linha["CATEGORIA_FREQ"] == "Rara":
        score += 2

    # ClinVar
    if linha["CLASSE_CLINVAR"] == "Patogênica":
        score += 6

    elif linha["CLASSE_CLINVAR"] == "Provavelmente Patogênica":
        score += 4

    elif linha["CLASSE_CLINVAR"] == "VUS":
        score += 2

    return score

df["SCORE"] = df.apply(calcular_score, axis=1)

print("Score calculado.")
print()
# =====================================================
# ORDENAÇÃO
# =====================================================

print("Ordenando variantes...")

df = df.sort_values(
    by=[
        "SCORE",
        "IMPACT",
        "GNOMAD_AF"
    ],
    ascending=[
        False,
        True,
        True
    ]
)

print("Ordenação concluída.")
print()

# =====================================================
# ESTATÍSTICAS
# =====================================================

print("=" * 70)
print("RESUMO DA BASE MESTRE")
print("=" * 70)

print(f"Total de variantes: {len(df):,}")
print()

print("Categorias de frequência:")

print(df["CATEGORIA_FREQ"].value_counts())

print()

print("Classificação ClinVar:")

print(df["CLASSE_CLINVAR"].value_counts())

print()

# =====================================================
# SALVA
# =====================================================

print("Salvando Base Mestre...")

df.to_excel(
    ARQUIVO_SAIDA,
    index=False,
    engine="xlsxwriter"
)

print()

print("=" * 70)
print("BASE MESTRE GERADA COM SUCESSO")
print("=" * 70)

print(f"Arquivo: {ARQUIVO_SAIDA}")
