#!/usr/bin/env python3
"""
Sistema de Gerenciamento de Clube de Desbravadores
Arquivo principal para executar a aplicação Flask
"""

import os
from app import create_app, db
from app.models import User, Desbravador, Mensalidade, Transacao, Evento
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Cria um usuário administrador padrão se não existir"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@desbravadores.com',
            password_hash=generate_password_hash('admin123'),
            nome_completo='Administrador do Sistema',
            cargo='Diretor'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário administrador criado:")
        print("   Usuário: admin")
        print("   Senha: admin123")
        print("   ⚠️  Altere a senha após o primeiro login!")

def create_sample_data():
    """Cria dados de exemplo para demonstração"""
    # Verificar se já existem dados
    if Desbravador.query.count() > 0:
        return
    
    print("📝 Criando dados de exemplo...")
    
    # Criar desbravadores de exemplo
    desbravadores_exemplo = [
        {
            'nome': 'João Silva',
            'idade': 12,
            'data_nascimento': '2011-05-15',
            'unidade': 'Companheiro',
            'classe': 'Companheiro',
            'telefone': '(11) 99999-1111',
            'email': 'joao@email.com',
            'endereco': 'Rua das Flores, 123',
            'nome_responsavel': 'Maria Silva',
            'telefone_responsavel': '(11) 99999-2222'
        },
        {
            'nome': 'Ana Santos',
            'idade': 14,
            'data_nascimento': '2009-08-22',
            'unidade': 'Pesquisador',
            'classe': 'Pesquisador',
            'telefone': '(11) 99999-3333',
            'email': 'ana@email.com',
            'endereco': 'Av. Principal, 456',
            'nome_responsavel': 'Carlos Santos',
            'telefone_responsavel': '(11) 99999-4444'
        },
        {
            'nome': 'Pedro Oliveira',
            'idade': 16,
            'data_nascimento': '2007-12-10',
            'unidade': 'Pioneiro',
            'classe': 'Pioneiro',
            'telefone': '(11) 99999-5555',
            'email': 'pedro@email.com',
            'endereco': 'Rua do Sol, 789',
            'nome_responsavel': 'Lucia Oliveira',
            'telefone_responsavel': '(11) 99999-6666'
        }
    ]
    
    from datetime import datetime as _dt
    from werkzeug.security import generate_password_hash
    
    for i, dados in enumerate(desbravadores_exemplo):
        # Converter data_nascimento para objeto date se vier como string
        if isinstance(dados.get('data_nascimento'), str):
            dados['data_nascimento'] = _dt.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        
        # Adicionar campos de login para o primeiro desbravador
        if i == 0:
            dados['username'] = 'joao.silva'
            dados['password_hash'] = generate_password_hash('123456')
            dados['pode_fazer_login'] = True
        elif i == 1:
            dados['username'] = 'ana.santos'
            dados['password_hash'] = generate_password_hash('123456')
            dados['pode_fazer_login'] = True
        
        desbravador = Desbravador(**dados)
        db.session.add(desbravador)
    
    db.session.commit()
    
    # Criar mensalidades de exemplo para o mês atual
    from datetime import datetime
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    desbravadores = Desbravador.query.all()
    for desbravador in desbravadores:
        mensalidade = Mensalidade(
            desbravador_id=desbravador.id,
            mes_referencia=mes_atual,
            ano_referencia=ano_atual,
            valor=50.0,
            status='pendente'
        )
        db.session.add(mensalidade)
    
    # Criar algumas transações de exemplo
    transacoes_exemplo = [
        {
            'tipo': 'receita',
            'categoria': 'mensalidade',
            'descricao': 'Mensalidade - João Silva',
            'valor': 50.0,
            'data_transacao': datetime.now()
        },
        {
            'tipo': 'despesa',
            'categoria': 'material',
            'descricao': 'Compra de material para atividades',
            'valor': 25.0,
            'data_transacao': datetime.now()
        },
        {
            'tipo': 'receita',
            'categoria': 'evento',
            'descricao': 'Arrecadação do acampamento',
            'valor': 200.0,
            'data_transacao': datetime.now()
        }
    ]
    
    for dados in transacoes_exemplo:
        transacao = Transacao(**dados)
        db.session.add(transacao)
    
    # Criar eventos de exemplo
    eventos_exemplo = [
        {
            'nome': 'Reunião Semanal',
            'descricao': 'Reunião regular do clube de desbravadores',
            'data_inicio': datetime.now().replace(day=1, hour=19, minute=0, second=0, microsecond=0),
            'local': 'Sede do Clube',
            'tipo': 'reunião'
        },
        {
            'nome': 'Acampamento de Fim de Semana',
            'descricao': 'Acampamento especial para todas as unidades',
            'data_inicio': datetime.now().replace(day=15, hour=8, minute=0, second=0, microsecond=0),
            'data_fim': datetime.now().replace(day=16, hour=17, minute=0, second=0, microsecond=0),
            'local': 'Parque Municipal',
            'tipo': 'acampamento',
            'custo': 25.0
        },
        {
            'nome': 'Especialidade de Culinária',
            'descricao': 'Aula prática de culinária ao ar livre',
            'data_inicio': datetime.now().replace(day=20, hour=14, minute=0, second=0, microsecond=0),
            'local': 'Área de Churrasqueira',
            'tipo': 'especialidade'
        }
    ]
    
    for dados in eventos_exemplo:
        evento = Evento(**dados)
        db.session.add(evento)
    
    db.session.commit()
    print("✅ Dados de exemplo criados com sucesso!")
    print("📋 Desbravadores com login:")
    print("   - João Silva: joao.silva / 123456")
    print("   - Ana Santos: ana.santos / 123456")

def main():
    """Função principal para executar a aplicação"""
    # Criar aplicação Flask
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas do banco de dados
        db.create_all()
        print("✅ Banco de dados inicializado!")
        
        # Criar usuário administrador
        create_admin_user()
        
        # Criar dados de exemplo (apenas se não existirem dados)
        create_sample_data()
    
    # Configurações do servidor
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n🚀 Iniciando Sistema de Desbravadores...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Modo Debug: {'Ativado' if debug else 'Desativado'}")
    print(f"\n📋 Instruções:")
    print(f"   1. Acesse a URL acima no seu navegador")
    print(f"   2. Faça login com: admin / admin123")
    print(f"   3. Altere a senha padrão nas configurações")
    print(f"   4. Explore os módulos do sistema")
    print(f"\n⏹️  Para parar o servidor: Ctrl+C")
    print("=" * 50)
    
    # Executar aplicação
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    main()
