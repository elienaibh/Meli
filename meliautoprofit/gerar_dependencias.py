"""
Script para gerar o arquivo de dependências
"""
import subprocess
import sys

def gerar_dependencias():
    """Gera o arquivo de dependências com base no ambiente virtual"""
    print("DEBUG: Gerando dependências")
    
    try:
        with open("dependencias.txt", "w") as f:
            subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f, check=True)
        print("DEBUG: Dependências geradas com sucesso")
        return True
    except Exception as e:
        print(f"DEBUG: Erro ao gerar dependências: {str(e)}")
        return False

if __name__ == "__main__":
    gerar_dependencias() 