import os
from storage import salvar_dados, carregar_dados
from ui import selecionar_1, selecionar_2, selecionar_3
from services import cadastrar, listar, buscar, atualizar, remover
from reports import menu_relatorios


# .------------------------------------------------------------------ #
#  CONSTANTES DE ARQUIVO
# ------------------------------------------------------------------ #
USUARIOS_ARQUIVO = "data/usuarios.json"
PROJETOS_ARQUIVO = "data/projetos.json"
TAREFAS_ARQUIVO  = "data/tarefas.json"


# ------------------------------------------------------------------ #
#  PREPARAÇÃO DO AMBIENTE
# ------------------------------------------------------------------ #
os.makedirs("data", exist_ok=True)

usuarios = carregar_dados(USUARIOS_ARQUIVO)
projetos = carregar_dados(PROJETOS_ARQUIVO)
tarefas  = carregar_dados(TAREFAS_ARQUIVO)

print("\n=== Sistema de Gerenciamento de Projetos ===")


# ------------------------------------------------------------------ #
#  FUNÇÕES AUXILIARES INTERNAS
# ------------------------------------------------------------------ #
def processar_entidade(tipo, lista, arquivo):
    """
    Reduz repetição do CRUD.
    tipo: 1 usuário | 2 projeto | 3 tarefa
    """
    acao = selecionar_2() if tipo in (1, 2) else selecionar_3()

    if acao == 1:  # Cadastrar
        item = cadastrar(tipo, usuarios, projetos, tarefas)
        if item:
            lista.append(item)
            salvar_dados(arquivo, lista)
            print("\nRegistro cadastrado!")

    elif acao == 2:  # Listar
        listar(tipo, usuarios, projetos, tarefas)

    elif acao == 3:  # Buscar (só 1 e 2 usam 5 opções)
        if tipo in (1, 2):
            buscar(tipo, usuarios, projetos, tarefas)
        else:
            if atualizar(tipo, usuarios, projetos, tarefas):
                salvar_dados(arquivo, lista)

    elif acao == 4:  # Atualizar / Remover
        if tipo in (1, 2):
            if atualizar(tipo, usuarios, projetos, tarefas):
                salvar_dados(arquivo, lista)
        else:
            if remover(tipo, usuarios, projetos, tarefas):
                salvar_dados(arquivo, lista)

    elif acao == 5:  # Remover (existe apenas p/ usuário e projeto)
        if remover(tipo, usuarios, projetos, tarefas):
            salvar_dados(arquivo, lista)


# ------------------------------------------------------------------ #
#  LOOP PRINCIPAL
# ------------------------------------------------------------------ #
while True:
    escolha = selecionar_1()

    if escolha == 1:  # Usuários
        processar_entidade(1, usuarios, USUARIOS_ARQUIVO)

    elif escolha == 2:  # Projetos
        processar_entidade(2, projetos, PROJETOS_ARQUIVO)

    elif escolha == 3:  # Tarefas
        processar_entidade(3, tarefas, TAREFAS_ARQUIVO)

    elif escolha == 4:  # Relatórios
        menu_relatorios(tarefas, projetos, usuarios)

    elif escolha == 5:
        print("\nSistema encerrado. Dados salvos.")
        break


