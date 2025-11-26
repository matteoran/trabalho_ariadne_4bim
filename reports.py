from datetime import datetime

def rel_resumo_projeto(tarefas, projetos):
    relatorio = {}
    nomes_projetos = {p["id"]: p["nome"] for p in projetos}
    
    for tarefa in tarefas:
        proj_id = tarefa.get("projeto_id")
        status = tarefa.get("status", "desconhecido").lower()
        
        if proj_id not in relatorio:
            relatorio[proj_id] = {
                "nome": nomes_projetos.get(proj_id, f"Projeto ID {proj_id} (N/A)"),
                "total": 0, "pendente": 0, "andamento": 0, "concluída": 0
            }
            
        relatorio[proj_id]["total"] += 1
        if status in relatorio[proj_id]:
            relatorio[proj_id][status] += 1

    print("\n--- RESUMO POR PROJETO ---")
    if not relatorio:
        print("Nenhuma tarefa encontrada.")
        return

    for proj_id, dados in relatorio.items():
        total = dados["total"]
        concluidas = dados["concluída"]
        percentual = (concluidas / total) * 100 if total > 0 else 0
        
        print(f"\nProjeto: {dados['nome']} (ID: {proj_id})")
        print(f"  Total: {total} | Concluídas: {concluidas} ({percentual:.1f}%)")
        print(f"  Pendente: {dados['pendente']} | Andamento: {dados['andamento']}")


def rel_produtividade_usuario(tarefas, usuarios):
    produtividade = {}
    nomes_usuarios = {u["id"]: u["nome"] for u in usuarios}
    
    for tarefa in tarefas:
        resp_id = tarefa.get("responsavel_id")
        status = tarefa.get("status", "").lower()
        
        if status == "concluída" and resp_id:
            if resp_id not in produtividade:
                produtividade[resp_id] = {
                    "nome": nomes_usuarios.get(resp_id, f"Usuário ID {resp_id} (N/A)"),
                    "concluidas": 0
                }
            produtividade[resp_id]["concluidas"] += 1

    print("\n--- PRODUTIVIDADE POR USUÁRIO ---")

    if not produtividade:
        print("Nenhuma tarefa concluída encontrada.")
        return

    for user_id, dados in produtividade.items():
        print(f"Usuário: {dados['nome']} (ID: {user_id})")
        print(f"  Tarefas Concluídas: {dados['concluidas']}")


def rel_tarefas_atrasadas(tarefas):
    hoje = datetime.now().date()
    atrasadas = []

    for tarefa in tarefas:
        prazo_str = tarefa.get("prazo")
        status = tarefa.get("status", "").lower()
        
        if status != "concluída":
            try:
                prazo = datetime.strptime(prazo_str, "%Y-%m-%d").date()
                if prazo < hoje:
                    atrasadas.append(tarefa)
            except (ValueError, TypeError):
                continue

    print("\n--- TAREFAS ATRASADAS ---")

    if not atrasadas:
        print("Nenhuma tarefa atrasada. Parabéns!")
        return

    for t in atrasadas:
        print(f"Tarefa: {t['titulo']} (ID: {t['id']})")
        print(f"  Prazo: {t['prazo']} | Status: {t['status']} | Responsável ID: {t['responsavel_id']}")

def menu_relatorios(tarefas, projetos, usuarios):
    while True:
        try:
            print("\nRELATÓRIOS:")
            print("1. Resumo por Projeto")
            print("2. Produtividade por Usuário")
            print("3. Tarefas Atrasadas")
            print("4. Voltar")
            
            x = int(input("Opção > "))
            
            if x == 1:
                rel_resumo_projeto(tarefas, projetos)
            elif x == 2:
                rel_produtividade_usuario(tarefas, usuarios)
            elif x == 3:
                rel_tarefas_atrasadas(tarefas)
            elif x == 4:
                break
            else:
                print("\nOpção inválida.")
        except ValueError:
            print("\nEntrada inválida. Digite o número da opção desejada.")