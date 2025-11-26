import json
import os

def salvar_dados(caminho_arquivo, dados):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {caminho_arquivo}")

def carregar_dados(caminho_arquivo):
    if not os.path.exists(caminho_arquivo) or os.path.getsize(caminho_arquivo) == 0:
        return []
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"ERRO: Arquivo {caminho_arquivo} contém JSON inválido. Retornando lista vazia.")
        return []