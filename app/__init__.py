from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inicialização do banco de dados
db = SQLAlchemy()

# Inicialização do gerenciador de login
login_manager = LoginManager()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desbravadores.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Configurar user_loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User, Desbravador
        # Tentar carregar como User primeiro
        user = User.query.get(int(user_id))
        if user:
            return user
        # Se não encontrar, tentar como Desbravador
        return Desbravador.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.desbravadores import desbravadores_bp
    from app.routes.financeiro import financeiro_bp
    from app.routes.relatorios import relatorios_bp
    from app.routes.desbravador import desbravador_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(desbravadores_bp, url_prefix='/desbravadores')
    app.register_blueprint(financeiro_bp, url_prefix='/financeiro')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
    app.register_blueprint(desbravador_bp)
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
