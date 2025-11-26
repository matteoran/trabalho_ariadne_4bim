from datetime import datetime
import re

def validar_email(email, lista_usuarios):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Formato de e-mail inválido."
    
    for usuario in lista_usuarios:
        if usuario.get("email", "").lower() == email.lower():
            return False, "E-mail já cadastrado."
    
    return True, ""

def validar_periodo(data_inicio, data_fim):
    try:
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim = datetime.strptime(data_fim, "%Y-%m-%d")
        
        if inicio > fim:
            return False, "Data de início deve ser menor ou igual à data de fim."
        
        return True, ""
    except ValueError:
        return False, "Formato de data inválido. Use YYYY-MM-DD."

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Formato de data inválido. Use YYYY-MM-DD."

def gerar_novo_id(prefixo, lista):
    maior_num = 0
    
    for item in lista:
        item_id = item.get("id", "")
        if item_id.startswith(prefixo + "_") and item_id[len(prefixo) + 1:].isdigit():
            try:
                num = int(item_id[len(prefixo) + 1:])
                if num > maior_num:
                    maior_num = num
            except ValueError:
                pass 
    
    novo_num = maior_num + 1
    return f"{prefixo}_{novo_num:03d}"