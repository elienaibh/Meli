"""
Testes para o serviço de preparação
"""
import os
import pytest
import tempfile
import csv
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from app.services.preparacao import PreparacaoService
from database.models import StatusProduto, Produto, Fornecedor

class TestPreparacaoService:
    """Testes para o serviço de preparação"""
    
    @pytest.fixture
    def service(self, test_db):
        """Fixture para criar o serviço de preparação"""
        service = PreparacaoService(test_db)
        return service
    
    def test_importar_produtos_csv_arquivo_inexistente(self, service):
        """Testa importação de um arquivo que não existe"""
        # Executa o método com um arquivo inexistente
        resultado = service.importar_produtos_csv("arquivo_inexistente.csv")
        
        # Deve retornar 0 indicando que nenhum produto foi importado
        assert resultado == 0
    
    def test_importar_produtos_csv(self, service, test_db, tmp_path):
        """Testa importação de produtos de um arquivo CSV"""
        # Cria um arquivo CSV temporário
        csv_path = tmp_path / "produtos_teste.csv"
        
        # Dados para o CSV
        produtos_csv = [
            {
                "titulo": "Produto Importado 1",
                "descricao": "Descrição do produto importado 1",
                "preco_custo": "100.50",
                "preco_venda": "199.99",
                "margem": "0.99",
                "estoque": "20",
                "categoria": "Importados",
                "sku": "IMP-001",
                "fornecedor": "cj_dropshipping",
                "fornecedor_product_id": "CJ-123456"
            },
            {
                "titulo": "Produto Importado 2",
                "descricao": "Descrição do produto importado 2",
                "preco_custo": "80.25",
                "preco_venda": "159.99",
                "estoque": "15",
                "categoria": "Importados",
                "sku": "IMP-002",
                "fornecedor": "spocket",
                "fornecedor_product_id": "SP-123456"
            }
        ]
        
        # Escreve o arquivo CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=produtos_csv[0].keys())
            writer.writeheader()
            writer.writerows(produtos_csv)
        
        # Executa o método
        resultado = service.importar_produtos_csv(str(csv_path))
        
        # Deve retornar 2 indicando que dois produtos foram importados
        assert resultado == 2
        
        # Verifica se os produtos foram salvos no banco
        produtos = test_db.query(Produto).filter(Produto.sku.in_(["IMP-001", "IMP-002"])).all()
        assert len(produtos) == 2
        
        # Verifica os dados do primeiro produto
        produto1 = next((p for p in produtos if p.sku == "IMP-001"), None)
        assert produto1 is not None
        assert produto1.titulo == "Produto Importado 1"
        assert produto1.preco_custo == 100.50
        assert produto1.preco_venda == 199.99
        assert produto1.margem == 0.99
        assert produto1.estoque == 20
        assert produto1.status == StatusProduto.PENDENTE
        
        # Verifica os dados do segundo produto (com margem calculada)
        produto2 = next((p for p in produtos if p.sku == "IMP-002"), None)
        assert produto2 is not None
        assert produto2.titulo == "Produto Importado 2"
        assert produto2.preco_custo == 80.25
        assert produto2.preco_venda == 159.99
        # Verifica se a margem foi calculada corretamente
        expected_margin = (159.99 - 80.25) / 80.25
        assert pytest.approx(produto2.margem, 0.01) == expected_margin
    
    def test_importar_produtos_csv_sem_fornecedores(self, service, test_db, tmp_path):
        """Testa importação sem fornecedores cadastrados"""
        # Remove os fornecedores do banco de teste
        for fornecedor in test_db.query(Fornecedor).all():
            test_db.delete(fornecedor)
        test_db.commit()
        
        # Cria um arquivo CSV temporário
        csv_path = tmp_path / "produtos_teste.csv"
        
        # Dados para o CSV
        produtos_csv = [
            {
                "titulo": "Produto Importado 1",
                "descricao": "Descrição do produto importado 1",
                "preco_custo": "100.50",
                "preco_venda": "199.99",
                "margem": "0.99",
                "estoque": "20",
                "categoria": "Importados",
                "sku": "IMP-001",
                "fornecedor": "cj_dropshipping",
                "fornecedor_product_id": "CJ-123456"
            }
        ]
        
        # Escreve o arquivo CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=produtos_csv[0].keys())
            writer.writeheader()
            writer.writerows(produtos_csv)
        
        # Executa o método
        resultado = service.importar_produtos_csv(str(csv_path))
        
        # Deve retornar 0 indicando que nenhum produto foi importado
        assert resultado == 0
    
    def test_criar_produtos_teste(self, service, test_db):
        """Testa a criação de produtos de teste"""
        # Executa o método para criar 10 produtos de teste
        quantidade = 10
        resultado = service.criar_produtos_teste(quantidade)
        
        # Deve retornar a quantidade de produtos criados
        assert resultado == quantidade
        
        # Verifica se os produtos foram salvos no banco
        produtos = test_db.query(Produto).filter(Produto.sku.like("TESTE-%")).all()
        assert len(produtos) >= quantidade  # Podem existir outros produtos de teste já criados
        
        # Verifica os produtos criados
        for i in range(1, quantidade + 1):
            sku = f"TESTE-{i:04d}"
            produto = next((p for p in produtos if p.sku == sku), None)
            
            # Pode não encontrar exatamente este SKU se já existirem outros produtos teste
            if produto:
                assert produto.titulo.startswith("Produto Teste")
                assert produto.status == StatusProduto.PENDENTE
                assert produto.preco_custo > 0
                assert produto.preco_venda > produto.preco_custo
    
    def test_criar_produtos_teste_sem_fornecedores(self, service, test_db):
        """Testa a criação de produtos de teste sem fornecedores cadastrados"""
        # Remove os fornecedores do banco de teste
        for fornecedor in test_db.query(Fornecedor).all():
            test_db.delete(fornecedor)
        test_db.commit()
        
        # Executa o método
        resultado = service.criar_produtos_teste(10)
        
        # Deve retornar 0 indicando que nenhum produto foi criado
        assert resultado == 0
    
    def test_fazer_backup_produtos(self, service, test_db, tmp_path):
        """Testa o backup de produtos para CSV"""
        # Cria alguns produtos adicionais para o teste
        produtos = [
            Produto(
                titulo="Produto Backup 1",
                descricao="Descrição do produto backup 1",
                preco_custo=120.0,
                preco_venda=240.0,
                margem=1.0,
                estoque=30,
                categoria="Backups",
                sku="BACKUP-001",
                fornecedor_id=1,
                status=StatusProduto.ATIVO
            ),
            Produto(
                titulo="Produto Backup 2",
                descricao="Descrição do produto backup 2",
                preco_custo=90.0,
                preco_venda=180.0,
                margem=1.0,
                estoque=25,
                categoria="Backups",
                sku="BACKUP-002",
                fornecedor_id=2,
                status=StatusProduto.PENDENTE
            )
        ]
        
        # Adiciona os produtos ao banco
        for produto in produtos:
            test_db.add(produto)
        test_db.commit()
        
        # Caminho para o arquivo de backup
        backup_path = tmp_path / "backup_produtos.csv"
        
        # Executa o método
        resultado = service.fazer_backup_produtos(str(backup_path))
        
        # Deve retornar True indicando sucesso
        assert resultado is True
        
        # Verifica se o arquivo foi criado
        assert os.path.exists(backup_path)
        
        # Verifica o conteúdo do arquivo
        with open(backup_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            linhas = list(reader)
            
            # Deve ter pelo menos os produtos que criamos
            assert len(linhas) >= 2
            
            # Verifica se os produtos que criamos estão no CSV
            skus = [linha["sku"] for linha in linhas]
            assert "BACKUP-001" in skus
            assert "BACKUP-002" in skus
            
            # Verifica os campos de um produto específico
            produto_backup = next((p for p in linhas if p["sku"] == "BACKUP-001"), None)
            assert produto_backup is not None
            assert produto_backup["titulo"] == "Produto Backup 1"
            assert float(produto_backup["preco_custo"]) == 120.0
            assert float(produto_backup["preco_venda"]) == 240.0
            assert float(produto_backup["margem"]) == 1.0
            assert int(produto_backup["estoque"]) == 30
            assert produto_backup["status"] == StatusProduto.ATIVO.value
    
    def test_fazer_backup_produtos_erro_arquivo(self, service, monkeypatch):
        """Testa o backup de produtos com erro ao escrever o arquivo"""
        # Mock para simular erro ao abrir o arquivo
        def mock_open_error(*args, **kwargs):
            raise IOError("Erro ao abrir arquivo")
        
        # Aplica o mock
        monkeypatch.setattr("builtins.open", mock_open_error)
        
        # Executa o método
        resultado = service.fazer_backup_produtos("backup_erro.csv")
        
        # Deve retornar False indicando falha
        assert resultado is False 