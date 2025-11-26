def selecionar_1():
    while True:
        try:
            x = int(input("\nGERENCIAR:\n 1. Usuários \n 2. Projetos \n 3. Tarefas \n 4. Relatórios \n 5. Sair \n > "))
            if 1 <= x <= 5:
                return x
            raise ValueError
        except ValueError:
            print("\nOpção inválida. Digite um número de 1 a 5.")

def selecionar_2():
    while True:
        try:
            y = int(input("\nO QUE FAZER?\n 1. Cadastrar \n 2. Listar \n 3. Buscar \n 4. Atualizar \n 5. Remover \n > "))
            if 1 <= y <= 5:
                return y
            raise ValueError
        except ValueError:
            print("\nOpção inválida. Digite um número de 1 a 5.")

def selecionar_3():
    while True:
        try:
            y = int(input("\nO QUE FAZER?\n 1. Cadastrar \n 2. Listar \n 3. Atualizar \n 4. Remover \n > "))
            if 1 <= y <= 4:
                return y
            raise ValueError
        except ValueError:

            print("\nOpção inválida. Digite um número de 1 a 4.")
