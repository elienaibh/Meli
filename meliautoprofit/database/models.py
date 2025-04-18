"""
Modelos do banco de dados
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class StatusProduto(enum.Enum):
    """Enum para status de produto"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    ESGOTADO = "esgotado"
    PENDENTE = "pendente"

class StatusPedido(enum.Enum):
    """Enum para status de pedido"""
    PENDENTE = "pendente"
    PAGO = "pago"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class Fornecedor(Base):
    """Modelo de fornecedor"""
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    api_type = Column(String(50), nullable=False)  # cj_dropshipping ou spocket
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="fornecedor")
    
    def __repr__(self):
        return f"<Fornecedor {self.nome}>"

class Produto(Base):
    """Modelo de produto"""
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    preco_custo = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    margem = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    categoria = Column(String(100))
    sku = Column(String(100), unique=True)
    ml_item_id = Column(String(100), unique=True)  # ID do item no Mercado Livre
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    fornecedor_product_id = Column(String(100))  # ID do produto no fornecedor
    status = Column(Enum(StatusProduto), default=StatusProduto.PENDENTE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    pedidos_items = relationship("PedidoItem", back_populates="produto")
    
    def __repr__(self):
        return f"<Produto {self.titulo}>"

class Cliente(Base):
    """Modelo de cliente"""
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    ml_user_id = Column(String(100), unique=True)
    nome = Column(String(255))
    email = Column(String(255))
    telefone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="cliente")
    enderecos = relationship("Endereco", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente {self.nome}>"

class Endereco(Base):
    """Modelo de endereço"""
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    rua = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)
    is_principal = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="enderecos")
    pedidos = relationship("Pedido", back_populates="endereco_entrega")
    
    def __repr__(self):
        return f"<Endereco {self.cep}>"

class Pedido(Base):
    """Modelo de pedido"""
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    ml_order_id = Column(String(100), unique=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    endereco_entrega_id = Column(Integer, ForeignKey("enderecos.id"))
    valor_total = Column(Float, nullable=False)
    valor_frete = Column(Float, default=0.0)
    valor_produtos = Column(Float, nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.PENDENTE)
    data_pedido = Column(DateTime, default=datetime.utcnow)
    data_pagamento = Column(DateTime)
    data_envio = Column(DateTime)
    data_entrega = Column(DateTime)
    codigo_rastreio = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="pedidos")
    endereco_entrega = relationship("Endereco", back_populates="pedidos")
    items = relationship("PedidoItem", back_populates="pedido")
    
    def __repr__(self):
        return f"<Pedido {self.ml_order_id}>"

class PedidoItem(Base):
    """Modelo de item de pedido"""
    __tablename__ = "pedidos_items"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    pedido = relationship("Pedido", back_populates="items")
    produto = relationship("Produto", back_populates="pedidos_items")
    
    def __repr__(self):
        return f"<PedidoItem {self.id}>"

class Relatorio(Base):
    """Modelo de relatório"""
    __tablename__ = "relatorios"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)  # diario, semanal, mensal
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    total_pedidos = Column(Integer, default=0)
    total_vendas = Column(Float, default=0.0)
    total_lucro = Column(Float, default=0.0)
    dados = Column(Text)  # JSON com dados detalhados
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Relatorio {self.tipo} {self.data_inicio.strftime('%Y-%m-%d')}>" 