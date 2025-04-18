"""
Repositórios para acesso ao banco de dados
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from . import models
from typing import List, Optional, Dict, Any
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

class ProdutoRepository:
    """Repositório para operações com produtos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, product_id: int) -> Optional[models.Produto]:
        """Obtém um produto pelo ID"""
        return self.db.query(models.Produto).filter(models.Produto.id == product_id).first()
    
    def get_by_sku(self, sku: str) -> Optional[models.Produto]:
        """Obtém um produto pelo SKU"""
        return self.db.query(models.Produto).filter(models.Produto.sku == sku).first()
    
    def get_by_ml_item_id(self, ml_item_id: str) -> Optional[models.Produto]:
        """Obtém um produto pelo ID do Mercado Livre"""
        return self.db.query(models.Produto).filter(models.Produto.ml_item_id == ml_item_id).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[models.Produto]:
        """Lista todos os produtos com paginação"""
        return self.db.query(models.Produto).offset(skip).limit(limit).all()
    
    def list_by_status(self, status: models.StatusProduto, skip: int = 0, limit: int = 100) -> List[models.Produto]:
        """Lista produtos por status"""
        return self.db.query(models.Produto).filter(models.Produto.status == status).offset(skip).limit(limit).all()
    
    def list_by_fornecedor(self, fornecedor_id: int, skip: int = 0, limit: int = 100) -> List[models.Produto]:
        """Lista produtos por fornecedor"""
        return self.db.query(models.Produto).filter(models.Produto.fornecedor_id == fornecedor_id).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[models.Produto]:
        """Busca produtos pelo título ou descrição"""
        search_query = f"%{query}%"
        return self.db.query(models.Produto).filter(
            or_(
                models.Produto.titulo.ilike(search_query),
                models.Produto.descricao.ilike(search_query)
            )
        ).offset(skip).limit(limit).all()
    
    def create(self, produto_data: Dict[str, Any]) -> models.Produto:
        """Cria um novo produto"""
        produto = models.Produto(**produto_data)
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto
    
    def update(self, produto_id: int, produto_data: Dict[str, Any]) -> Optional[models.Produto]:
        """Atualiza um produto existente"""
        produto = self.get_by_id(produto_id)
        if produto:
            for key, value in produto_data.items():
                setattr(produto, key, value)
            self.db.commit()
            self.db.refresh(produto)
        return produto
    
    def delete(self, produto_id: int) -> bool:
        """Remove um produto"""
        produto = self.get_by_id(produto_id)
        if produto:
            self.db.delete(produto)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """Conta o número total de produtos"""
        return self.db.query(models.Produto).count()
    
    def count_by_status(self, status: models.StatusProduto) -> int:
        """Conta o número de produtos por status"""
        return self.db.query(models.Produto).filter(models.Produto.status == status).count()

class FornecedorRepository:
    """Repositório para operações com fornecedores"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, fornecedor_id: int) -> Optional[models.Fornecedor]:
        """Obtém um fornecedor pelo ID"""
        return self.db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()
    
    def get_by_api_type(self, api_type: str) -> Optional[models.Fornecedor]:
        """Obtém um fornecedor pelo tipo de API"""
        return self.db.query(models.Fornecedor).filter(models.Fornecedor.api_type == api_type).first()
    
    def list_all(self) -> List[models.Fornecedor]:
        """Lista todos os fornecedores"""
        return self.db.query(models.Fornecedor).all()
    
    def create(self, fornecedor_data: Dict[str, Any]) -> models.Fornecedor:
        """Cria um novo fornecedor"""
        fornecedor = models.Fornecedor(**fornecedor_data)
        self.db.add(fornecedor)
        self.db.commit()
        self.db.refresh(fornecedor)
        return fornecedor
    
    def update(self, fornecedor_id: int, fornecedor_data: Dict[str, Any]) -> Optional[models.Fornecedor]:
        """Atualiza um fornecedor existente"""
        fornecedor = self.get_by_id(fornecedor_id)
        if fornecedor:
            for key, value in fornecedor_data.items():
                setattr(fornecedor, key, value)
            self.db.commit()
            self.db.refresh(fornecedor)
        return fornecedor
    
    def delete(self, fornecedor_id: int) -> bool:
        """Remove um fornecedor"""
        fornecedor = self.get_by_id(fornecedor_id)
        if fornecedor:
            self.db.delete(fornecedor)
            self.db.commit()
            return True
        return False

class PedidoRepository:
    """Repositório para operações com pedidos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, pedido_id: int) -> Optional[models.Pedido]:
        """Obtém um pedido pelo ID"""
        return self.db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    
    def get_by_ml_order_id(self, ml_order_id: str) -> Optional[models.Pedido]:
        """Obtém um pedido pelo ID do Mercado Livre"""
        return self.db.query(models.Pedido).filter(models.Pedido.ml_order_id == ml_order_id).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[models.Pedido]:
        """Lista todos os pedidos com paginação"""
        return self.db.query(models.Pedido).order_by(desc(models.Pedido.data_pedido)).offset(skip).limit(limit).all()
    
    def list_by_status(self, status: models.StatusPedido, skip: int = 0, limit: int = 100) -> List[models.Pedido]:
        """Lista pedidos por status"""
        return self.db.query(models.Pedido).filter(models.Pedido.status == status).order_by(desc(models.Pedido.data_pedido)).offset(skip).limit(limit).all()
    
    def list_by_cliente(self, cliente_id: int, skip: int = 0, limit: int = 100) -> List[models.Pedido]:
        """Lista pedidos por cliente"""
        return self.db.query(models.Pedido).filter(models.Pedido.cliente_id == cliente_id).order_by(desc(models.Pedido.data_pedido)).offset(skip).limit(limit).all()
    
    def create(self, pedido_data: Dict[str, Any]) -> models.Pedido:
        """Cria um novo pedido"""
        pedido = models.Pedido(**pedido_data)
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
    
    def update(self, pedido_id: int, pedido_data: Dict[str, Any]) -> Optional[models.Pedido]:
        """Atualiza um pedido existente"""
        pedido = self.get_by_id(pedido_id)
        if pedido:
            for key, value in pedido_data.items():
                setattr(pedido, key, value)
            self.db.commit()
            self.db.refresh(pedido)
        return pedido
    
    def delete(self, pedido_id: int) -> bool:
        """Remove um pedido"""
        pedido = self.get_by_id(pedido_id)
        if pedido:
            self.db.delete(pedido)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """Conta o número total de pedidos"""
        return self.db.query(models.Pedido).count()
    
    def count_by_status(self, status: models.StatusPedido) -> int:
        """Conta o número de pedidos por status"""
        return self.db.query(models.Pedido).filter(models.Pedido.status == status).count()
    
    def add_item(self, pedido_id: int, produto_id: int, quantidade: int, preco_unitario: float) -> models.PedidoItem:
        """Adiciona um item ao pedido"""
        item = models.PedidoItem(
            pedido_id=pedido_id,
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_items(self, pedido_id: int) -> List[models.PedidoItem]:
        """Obtém os itens de um pedido"""
        return self.db.query(models.PedidoItem).filter(models.PedidoItem.pedido_id == pedido_id).all()

class ClienteRepository:
    """Repositório para operações com clientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, cliente_id: int) -> Optional[models.Cliente]:
        """Obtém um cliente pelo ID"""
        return self.db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    
    def get_by_ml_user_id(self, ml_user_id: str) -> Optional[models.Cliente]:
        """Obtém um cliente pelo ID do Mercado Livre"""
        return self.db.query(models.Cliente).filter(models.Cliente.ml_user_id == ml_user_id).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[models.Cliente]:
        """Lista todos os clientes com paginação"""
        return self.db.query(models.Cliente).offset(skip).limit(limit).all()
    
    def create(self, cliente_data: Dict[str, Any]) -> models.Cliente:
        """Cria um novo cliente"""
        cliente = models.Cliente(**cliente_data)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    def update(self, cliente_id: int, cliente_data: Dict[str, Any]) -> Optional[models.Cliente]:
        """Atualiza um cliente existente"""
        cliente = self.get_by_id(cliente_id)
        if cliente:
            for key, value in cliente_data.items():
                setattr(cliente, key, value)
            self.db.commit()
            self.db.refresh(cliente)
        return cliente
    
    def delete(self, cliente_id: int) -> bool:
        """Remove um cliente"""
        cliente = self.get_by_id(cliente_id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
    
    def add_endereco(self, cliente_id: int, endereco_data: Dict[str, Any]) -> models.Endereco:
        """Adiciona um endereço ao cliente"""
        endereco_data["cliente_id"] = cliente_id
        endereco = models.Endereco(**endereco_data)
        self.db.add(endereco)
        self.db.commit()
        self.db.refresh(endereco)
        return endereco
    
    def get_enderecos(self, cliente_id: int) -> List[models.Endereco]:
        """Obtém os endereços de um cliente"""
        return self.db.query(models.Endereco).filter(models.Endereco.cliente_id == cliente_id).all()
    
    def get_endereco_principal(self, cliente_id: int) -> Optional[models.Endereco]:
        """Obtém o endereço principal de um cliente"""
        return self.db.query(models.Endereco).filter(
            and_(
                models.Endereco.cliente_id == cliente_id,
                models.Endereco.is_principal == True
            )
        ).first() 