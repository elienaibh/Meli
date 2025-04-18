#!/usr/bin/env python
"""
Script para executar os testes unitários
"""
import os
import sys
import argparse
import subprocess
import coverage

def main():
    """Função principal para executar os testes"""
    parser = argparse.ArgumentParser(description="Executa os testes unitários do MeliAutoProfit")
    parser.add_argument('--cov', action='store_true', help='Gera relatório de cobertura de código')
    parser.add_argument('--html', action='store_true', help='Gera relatório HTML de cobertura')
    parser.add_argument('--module', type=str, help='Módulo específico para testar (ex: test_preparacao_service)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    args = parser.parse_args()
    
    # Diretório base do projeto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Configura o caminho
    sys.path.insert(0, base_dir)
    
    # Comando base para pytest
    cmd = ["pytest"]
    
    # Adiciona flags ao comando
    if args.verbose:
        cmd.append("-v")
    
    # Configuração de cobertura
    if args.cov:
        cmd.extend(["--cov=app", "--cov=database"])
        if args.html:
            cmd.append("--cov-report=html")
        else:
            cmd.append("--cov-report=term")
    
    # Adiciona módulo específico se informado
    if args.module:
        cmd.append(f"tests/{args.module}.py")
    else:
        cmd.append("tests/")
    
    # Executa os testes
    print(f"Executando comando: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=base_dir)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main()) 