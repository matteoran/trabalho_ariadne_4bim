from utils import validar_email, validar_periodo, validar_data, gerar_novo_id

def criar_usuario(nome, email, perfil, lista_usuarios):
    if not nome.strip():
        return None, "Nome não pode ser vazio."

    valido, mensagem = validar_email(email, lista_usuarios)
    if not valido:
        return None, mensagem
    
    perfis_validos = ["admin", "membro", "gerente"]
    perfil_final = perfil.lower() if perfil.lower() in perfis_validos else "membro"
        
    novo_id = gerar_novo_id("u", lista_usuarios)
    
    usuario = {
        "id": novo_id,
        "nome": nome.strip(),
        "email": email.lower(),
        "perfil": perfil_final
    }
    return usuario, "Usuário criado com sucesso!"

def criar_projeto(nome, descricao, data_inicio, data_fim, lista_projetos):
    
    if not nome.strip():
        return None, "Nome do projeto não pode ser vazio."
    
    for projeto in lista_projetos:
        if projeto.get("nome", "").lower() == nome.strip().lower():
            return None, "Nome do projeto já existe."

    valido, mensagem = validar_periodo(data_inicio, data_fim)
    if not valido:
        return None, mensagem

    novo_id = gerar_novo_id("p", lista_projetos)

    projeto = {
        "id": novo_id,
        "nome": nome.strip(),
        "descricao": descricao.strip(),
        "inicio": data_inicio,
        "fim": data_fim
    }
    return projeto, "Projeto criado com sucesso!"

def criar_tarefa(titulo, projeto_id, responsavel_id, status, data_prazo, lista_tarefas, lista_projetos, lista_usuarios):
    
    if not titulo.strip():
        return None, "Título da tarefa não pode ser vazio."

    projeto_existe = any(p["id"] == projeto_id for p in lista_projetos)
    if not projeto_existe:
        return None, "ID do projeto não encontrado."
        
    responsavel_existe = any(u["id"] == responsavel_id for u in lista_usuarios)
    if not responsavel_existe:
        return None, "ID do responsável não encontrado."

    status_validos = ["pendente", "andamento", "concluída"]
    if status.lower() not in status_validos:
        return None, f"Status inválido. Use um de: {', '.join(status_validos)}."
        
    valido, mensagem = validar_data(data_prazo)
    if not valido:
        return None, mensagem

    novo_id = gerar_novo_id("t", lista_tarefas)

    tarefa = {
        "id": novo_id,
        "titulo": titulo.strip(),
        "projeto_id": projeto_id,
        "responsavel_id": responsavel_id,
        "status": status.lower(),
        "prazo": data_prazo
    }

    return tarefa, "Tarefa criada com sucesso!"
