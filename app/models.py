from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """Modelo para usuários do sistema (administradores)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    nome_completo = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)  # Diretor, Secretário, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Desbravador(UserMixin, db.Model):
    """Modelo para desbravadores"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    unidade = db.Column(db.String(50), nullable=False)  # Amigo, Companheiro, etc.
    classe = db.Column(db.String(50), nullable=False)  # Amigo, Companheiro, Pesquisador, etc.
    especialidades = db.Column(db.Text)  # JSON string com especialidades
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    endereco = db.Column(db.Text)
    nome_responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Campos para login
    username = db.Column(db.String(80), unique=True)  # Username único para login
    password_hash = db.Column(db.String(120))  # Hash da senha
    pode_fazer_login = db.Column(db.Boolean, default=False)  # Se pode fazer login
    
    # Relacionamento com mensalidades
    mensalidades = db.relationship('Mensalidade', backref='desbravador', lazy=True)
    
    def __repr__(self):
        return f'<Desbravador {self.nome}>'

class Mensalidade(db.Model):
    """Modelo para controle de mensalidades"""
    id = db.Column(db.Integer, primary_key=True)
    desbravador_id = db.Column(db.Integer, db.ForeignKey('desbravador.id'), nullable=False)
    mes_referencia = db.Column(db.Integer, nullable=False)  # 1-12
    ano_referencia = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False, default=0.0)
    data_pagamento = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, atrasado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Mensalidade {self.desbravador_id} - {self.mes_referencia}/{self.ano_referencia}>'

class Transacao(db.Model):
    """Modelo para transações financeiras"""
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # receita, despesa
    categoria = db.Column(db.String(50), nullable=False)  # mensalidade, evento, material, etc.
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_transacao = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transacao {self.tipo} - {self.valor}>'

class Evento(db.Model):
    """Modelo para eventos do clube"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime)
    local = db.Column(db.String(200))
    tipo = db.Column(db.String(50))  # acampamento, reunião, especialidade, etc.
    custo = db.Column(db.Float, default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Evento {self.nome}>'
