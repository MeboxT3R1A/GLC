# Configurações do Sistema de Desbravadores
# Arquivo de configuração para diferentes ambientes

import os
from datetime import timedelta

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-desenvolvimento'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configurações de upload (futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'app/static/uploads'
    
    # Configurações de email (futuro)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações de relatórios
    REPORTS_FOLDER = 'app/static/reports'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///desbravadores_dev.db'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///desbravadores.db'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log de erros por email
        import logging
        from logging.handlers import SMTPHandler
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Erro no Sistema de Desbravadores',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///desbravadores_test.db'
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
