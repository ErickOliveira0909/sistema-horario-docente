import secrets
import json

# Gerar uma chave secreta
def criar_key():
        
    key = secrets.token_hex(24)  # Exemplo: 'e5f692d5d7ae46ba9f7d234ea23ab99e'
    dados = {"SECRET_KEY": key}

    with open("key.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def get_key():
    with open("app/key.json", "r") as arquivo:
        dados = json.load(arquivo)
    return dados