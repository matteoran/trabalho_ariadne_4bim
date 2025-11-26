from datetime import datetime
from models import criar_usuario, criar_projeto, criar_tarefa
from utils import validar_data, validar_periodo, validar_email

def achar_usuario(usuarios, chave):
    chave_lower = chave.lower()
    for usuario in usuarios:
        if usuario.get("nome", "").lower() == chave_lower or \
           usuario.get("email", "").lower() == chave_lower:
            return usuario
    return None

def achar_projeto(projetos, nome):
    nome_lower = nome.lower()
    for projeto in projetos:
        if projeto.get("nome", "").lower() == nome_lower:
            return projeto
    return None

# --- C (CADASTRO) ---

def cadastrar(y, usuarios, projetos, tarefas):
    
    if y == 1:
        print("\n--- NOVO USUÁRIO ---")
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        perfil = input("Perfil (admin, membro, gerente): ").strip()

        novo_usuario, msg = criar_usuario(nome, email, perfil, usuarios)
        
        if novo_usuario is None:
            print(f"\nERRO: {msg}")
            return None
        return novo_usuario
    
    elif y == 2:
        print("\n--- NOVO PROJETO ---")
        nome = input("Nome: ").strip()
        descricao = input("Descrição: ").strip()
        data_inicio = input("Data de Início (YYYY-MM-DD): ").strip()
        data_fim = input("Data de Fim (YYYY-MM-DD): ").strip()
        
        novo_projeto, msg = criar_projeto(nome, descricao, data_inicio, data_fim, projetos)
        
        if novo_projeto is None:
            print(f"\nERRO: {msg}")
            return None
        return novo_projeto

    elif y == 3:
        print("\n--- NOVA TAREFA ---")
        if not projetos or not usuarios:
            print("\nERRO: Cadastre projetos e usuários primeiro.")
            return None
        
        titulo = input("Título: ").strip()
        proj_id = input("ID do Projeto (Ex: p_001): ").strip()
        resp_id = input("ID do Responsável (Ex: u_001): ").strip()
        status = input("Status (pendente, andamento, concluída): ").strip()
        data_prazo = input("Prazo (YYYY-MM-DD): ").strip()

        nova_tarefa, msg = criar_tarefa(titulo, proj_id, resp_id, status, data_prazo, tarefas, projetos, usuarios)
        
        if nova_tarefa is None:
            print(f"\nERRO: {msg}")
            return None
        return nova_tarefa
    
    return None

# --- R (LISTAR) ---

def listar(y, usuarios, projetos, tarefas):
    
    if y == 1:
        print("\n--- LISTA DE USUÁRIOS ---")
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
        for u in usuarios:
            print(f"ID: {u.get('id')} | Nome: {u.get('nome')} | Email: {u.get('email')} | Perfil: {u.get('perfil')}")
    
    elif y == 2:
        print("\n--- LISTA DE PROJETOS ---")
        if not projetos:
            print("Nenhum projeto cadastrado.")
            return
        for p in projetos:
            print(f"ID: {p.get('id')} | Nome: {p.get('nome')} | Início: {p.get('inicio')} | Fim: {p.get('fim')}")
            print(f"  Descrição: {p.get('descricao')}")
            print("-" * 20)
            
    elif y == 3:
        print("\n--- LISTA DE TAREFAS ---")
        if not tarefas:
            print("Nenhuma tarefa cadastrada.")
            return
            
        while True:
            try:
                filtro = int(input("\nListar por:\n 1. Projeto (ID)\n 2. Responsável (ID)\n 3. Status\n 4. Todas\n > "))
                if 1 <= filtro <= 4: break
                raise ValueError
            except ValueError:
                print("\nOpção inválida. Digite 1, 2, 3 ou 4.")

        tarefas_filtradas = []
        if filtro == 1:
            busca_id = input("Digite o ID do projeto: ").strip()
            tarefas_filtradas = [t for t in tarefas if t.get("projeto_id", "").lower() == busca_id.lower()]
            
        elif filtro == 2:
            busca_id = input("Digite o ID do responsável: ").strip()
            tarefas_filtradas = [t for t in tarefas if t.get("responsavel_id", "").lower() == busca_id.lower()]
            
        elif filtro == 3:
            busca_status = input("Digite o status: ").strip()
            tarefas_filtradas = [t for t in tarefas if t.get("status", "").lower() == busca_status.lower()]
            
        elif filtro == 4:
            tarefas_filtradas = tarefas

        if not tarefas_filtradas:
            print("\nNenhuma tarefa encontrada com este filtro.")
        else:
            for t in tarefas_filtradas:
                print(f"ID: {t.get('id')} | Título: {t.get('titulo')} | Status: {t.get('status')}")
                print(f"  Prazo: {t.get('prazo')} | Projeto ID: {t.get('projeto_id')} | Responsável ID: {t.get('responsavel_id')}")
                print("-" * 20)

# --- R (BUSCAR) ---
def buscar(y, usuarios, projetos, tarefas):
    
    if y == 1:
        print("\n--- BUSCAR USUÁRIO ---")
        chave = input("Digite o nome ou e-mail: ").strip()
        usuario = achar_usuario(usuarios, chave)
        if usuario:
            print("\nUsuário encontrado!")
            print(f"ID: {usuario.get('id')} | Nome: {usuario.get('nome')} | Email: {usuario.get('email')} | Perfil: {usuario.get('perfil')}")
            return usuario
        else:
            print("\nUsuário não encontrado!")
            return None
            
    elif y == 2:
        print("\n--- BUSCAR PROJETO ---")
        nome = input("Digite o nome do projeto: ").strip()
        projeto = achar_projeto(projetos, nome)
        if projeto:
            print("\nProjeto encontrado!")
            print(f"ID: {projeto.get('id')} | Nome: {projeto.get('nome')} | Início: {projeto.get('inicio')} | Fim: {projeto.get('fim')}")
            print(f"  Descrição: {projeto.get('descricao')}")
            return projeto
        else:
            print("\nProjeto não encontrado!")
            return None
    
    elif y == 3: 
        print("\n--- BUSCAR TAREFA ---")
        titulo_busca = input("Digite o TÍTULO da tarefa: ").strip().lower()
        
        tarefas_encontradas = [t for t in tarefas if t.get("titulo", "").lower() == titulo_busca]
        
        if tarefas_encontradas:
            print("\nTarefas encontradas:")
            for t in tarefas_encontradas:
                print(f"ID: {t.get('id')} | Título: {t.get('titulo')} | Status: {t.get('status')} | Prazo: {t.get('prazo')}")
            return tarefas_encontradas 
        else:
            print("\nTarefa não encontrada!")
            return None


# --- U (ATUALIZAR) ---
def atualizar(y, usuarios, projetos, tarefas):
    
    if y == 1:
        chave = input("\nDigite o nome ou e-mail do usuário para ATUALIZAR: ").strip()
        usuario = achar_usuario(usuarios, chave)
        
        if not usuario:
            print("\nUsuário não encontrado.")
            return False
            
        print("\nUsuário atual: ", usuario)
        
        while True:
            try:
                opcao_campo = int(input("\nAtualizar:\n 1. Nome \n 2. E-mail \n 3. Perfil \n > "))
                if 1 <= opcao_campo <= 3: break
                raise ValueError
            except ValueError:
                print("\nOpção inválida. Digite 1, 2 ou 3.")

        if opcao_campo == 1: campo, campo_nome = "nome", "nome"
        elif opcao_campo == 2: campo, campo_nome = "email", "e-mail"
        else: campo, campo_nome = "perfil", "perfil"
        
        novo_valor = input(f"Novo {campo_nome}: ").strip()
        
        if campo == "email":
            outros = [u for u in usuarios if u["id"] != usuario["id"]]
            valido, msg = validar_email(novo_valor, outros)
            if not valido:
                print(f"\nErro de validação: {msg}")
                return False
        
        usuario[campo] = novo_valor
        print("\nUsuário atualizado com sucesso!")
        return True 
        
    elif y == 2:
        nome_busca = input("\nDigite o nome do projeto para ATUALIZAR: ").strip()
        projeto = achar_projeto(projetos, nome_busca)

        if not projeto:
            print("\nProjeto não encontrado.")
            return False
            
        print("\nProjeto atual: ", projeto)
        
        while True:
            try:
                opcao_campo = int(input("\nAtualizar:\n 1. Nome \n 2. Descrição \n 3. Data de início (YYYY-MM-DD) \n 4. Data de fim (YYYY-MM-DD) \n > "))
                if 1 <= opcao_campo <= 4: break
                raise ValueError
            except ValueError:
                print("\nOpção inválida. Digite 1, 2, 3 ou 4.")
                
        if opcao_campo == 1: campo, campo_nome = "nome", "nome"
        elif opcao_campo == 2: campo, campo_nome = "descricao", "descrição"
        elif opcao_campo == 3: campo, campo_nome = "inicio", "data de início"
        else: campo, campo_nome = "fim", "data de fim"
        
        novo_valor = input(f"Novo {campo_nome}: ").strip()
        
        if campo == "nome":
            if not novo_valor:
                print("\nErro: Nome não pode ser vazio.")
                return False
            outros = [p for p in projetos if p["id"] != projeto["id"]]
            if any(p["nome"].lower() == novo_valor.lower() for p in outros):
                print("\nErro: Nome do projeto já existe.")
                return False
        
        if campo == "inicio" or campo == "fim":
            data_inicio = novo_valor if campo == "inicio" else projeto.get("inicio")
            data_fim = novo_valor if campo == "fim" else projeto.get("fim")
            
            valido, msg = validar_periodo(data_inicio, data_fim)
            if not valido:
                print(f"\nErro de validação: {msg}")
                return False

        projeto[campo] = novo_valor
        print("\nProjeto atualizado com sucesso!")
        return True
        
    elif y == 3:
        titulo_busca = input("\nDigite o título da tarefa para ATUALIZAR: ").strip()
        
        tarefa = next((t for t in tarefas if t.get("titulo", "").lower() == titulo_busca.lower()), None)
        
        if not tarefa:
            print("\nTarefa não encontrada.")
            return False
            
        print("\nTarefa atual: ", tarefa)
        
        while True:
            try:
                opcao_campo = int(input("\nAtualizar:\n 1. Título \n 2. Status \n 3. Responsável (ID) \n 4. Prazo (YYYY-MM-DD) \n 5. CONCLUIR \n 6. REABRIR \n > "))
                if 1 <= opcao_campo <= 6: break
                raise ValueError
            except ValueError:
                print("\nOpção inválida.")

        if opcao_campo == 5:
            tarefa["status"] = "concluída"
            print("\nTarefa CONCLUÍDA.")
            return True
        elif opcao_campo == 6:
            tarefa["status"] = "pendente"
            print("\nTarefa REABERTA (Pendente).")
            return True
        
        if opcao_campo == 1: campo, campo_nome = "titulo", "título"
        elif opcao_campo == 2: campo, campo_nome = "status", "status"
        elif opcao_campo == 3: campo, campo_nome = "responsavel_id", "ID do responsável"
        else: campo, campo_nome = "prazo", "prazo"
        
        novo_valor = input(f"Novo {campo_nome}: ").strip()
        
        if campo == "status":
            status_validos = ["pendente", "andamento", "concluída"]
            if novo_valor.lower() not in status_validos:
                print(f"\nErro: Status inválido. Use um de: {', '.join(status_validos)}.")
                return False
        elif campo == "prazo":
            valido, msg = validar_data(novo_valor)
            if not valido:
                print(f"\nErro de validação: {msg}")
                return False
        elif campo == "responsavel_id":
            responsavel_existe = any(u["id"] == novo_valor for u in usuarios)
            if not responsavel_existe:
                print("\nErro: ID do responsável não encontrado.")
                return False

        tarefa[campo] = novo_valor
        print("\nTarefa atualizada com sucesso!")
        return True
    
    return False

# --- D (REMOVER) ---
def remover(y, usuarios, projetos, tarefas):
    
    if y == 1:
        chave = input("\nDigite o nome ou e-mail do Usuário para REMOVER: ").strip()
        usuario = achar_usuario(usuarios, chave)
        
        if not usuario:
            print("\nUsuário não encontrado!")
            return False
            
        print("\nUsuário encontrado: ", usuario)
        
        usuario_id = usuario["id"]
        tarefas_vinculadas = [t for t in tarefas if t.get("responsavel_id") == usuario_id]
        if tarefas_vinculadas:
            print(f"\nAVISO: O usuário tem {len(tarefas_vinculadas)} tarefa(s) vinculada(s).")
            
        try:
            confirmar = int(input("\nConfirmar remoção?\n 1. Sim \n 2. Não \n > "))
        except ValueError:
            print("\nOpção inválida. Cancelando.")
            return False
            
        if confirmar == 1:
            usuarios.remove(usuario)
            print("\nUsuário removido!")
            return True
        else:
            print("\nOperação cancelada.")
            return False
            
    elif y == 2:
        nome_busca = input("\nDigite o nome do Projeto para REMOVER: ").strip()
        projeto = achar_projeto(projetos, nome_busca)
        
        if not projeto:
            print("\nProjeto não encontrado!")
            return False
            
        print("\nProjeto encontrado: ", projeto)
        
        projeto_id = projeto["id"]
        tarefas_vinculadas = [t for t in tarefas if t.get("projeto_id") == projeto_id]
        if tarefas_vinculadas:
            print(f"\nAVISO: O projeto tem {len(tarefas_vinculadas)} tarefa(s) vinculada(s).")
            
        try:
            confirmar = int(input("\nConfirmar remoção?\n 1. Sim \n 2. Não \n > "))
        except ValueError:
            print("\nOpção inválida. Cancelando.")
            return False
            
        if confirmar == 1:
            projetos.remove(projeto)
            print("\nProjeto removido!")
            return True
        else:
            print("\nOperação cancelada.")
            return False
            
    elif y == 3:
        titulo_busca = input("\nDigite o Título da Tarefa para REMOVER: ").strip()
        
        tarefa = next((t for t in tarefas if t.get("titulo", "").lower() == titulo_busca.lower()), None)
        
        if not tarefa:
            print("\nTarefa não encontrada!")
            return False
            
        print("\nTarefa encontrada: ", tarefa)
        
        try:
            confirmar = int(input("\nConfirmar remoção?\n 1. Sim \n 2. Não \n > "))
        except ValueError:
            print("\nOpção inválida. Cancelando.")
            return False
            
        if confirmar == 1:
            tarefas.remove(tarefa)
            print("\nTarefa removida!")
            return True
        else:
            print("\nOperação cancelada.")
            return False
            
    return False