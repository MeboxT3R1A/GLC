# Sistema de Gerenciamento de Clube de Desbravadores

Um sistema web completo para gerenciar clubes de desbravadores, desenvolvido com Python Flask e tema escuro moderno.

## 🎯 Funcionalidades

### ✅ Implementadas
- **Autenticação de usuários** com sistema de login seguro
- **Dashboard principal** com estatísticas em tempo real
- **Cadastro de desbravadores** com informações completas
- **Controle de mensalidades** com status de pagamento
- **Gestão financeira** com receitas e despesas
- **Relatórios** de mensalidades, fluxo de caixa e patrimônio
- **Interface responsiva** com tema escuro (azul, amarelo e preto)
- **Dados de exemplo** para demonstração

### 🚀 Futuras Melhorias
- Exportação de relatórios (PDF, Excel)
- Sistema de eventos e atividades
- Controle de especialidades
- Notificações por email
- Backup automático
- API REST para integrações

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+ com Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Flask-Login
- **ORM**: SQLAlchemy
- **Tema**: Escuro com cores azul, amarelo e preto

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de instalação

1. **Clone ou baixe o projeto**
```bash
# Se usando Git
git clone <url-do-repositorio>
cd sistema-desbravadores

# Ou simplesmente extraia os arquivos para uma pasta
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python run.py
```

4. **Acesse o sistema**
- Abra seu navegador em: `http://127.0.0.1:5000`
- **Login padrão**: `admin` / `admin123`
- ⚠️ **Altere a senha após o primeiro login!**

## 🎨 Interface

### Tema Visual
- **Cores principais**: Azul (#1e3a8a), Amarelo (#fbbf24), Preto (#1a1a1a)
- **Design**: Moderno, limpo e responsivo
- **Navegação**: Sidebar lateral com menu intuitivo
- **Cards**: Estatísticas com gradientes e animações

### Telas Principais
1. **Login** - Autenticação segura
2. **Dashboard** - Visão geral com estatísticas
3. **Desbravadores** - Cadastro e listagem de membros
4. **Financeiro** - Controle de mensalidades e transações
5. **Relatórios** - Análises e exportações

## 📊 Estrutura do Banco de Dados

### Tabelas Principais
- **users** - Usuários do sistema (administradores)
- **desbravadores** - Membros do clube
- **mensalidades** - Controle de pagamentos mensais
- **transacoes** - Receitas e despesas
- **eventos** - Atividades do clube (futuro)

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///desbravadores.db
```

### Personalização
- **Cores**: Edite `app/static/css/style.css`
- **Logo**: Substitua o ícone na navbar
- **Valores**: Modifique valores padrão nas rotas

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- 💻 Desktop (1200px+)
- 📱 Tablet (768px - 1199px)
- 📱 Mobile (até 767px)

## 🔒 Segurança

- Senhas criptografadas com Werkzeug
- Sessões seguras com Flask-Login
- Validação de dados nos formulários
- Proteção contra CSRF (futuro)

## 🚀 Deploy em Produção

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Usando Docker (futuro)
```bash
# Dockerfile será criado em versão futura
docker build -t sistema-desbravadores .
docker run -p 5000:5000 sistema-desbravadores
```

## 📈 Monitoramento

### Logs
- Logs de erro são salvos automaticamente
- Debug mode mostra erros detalhados
- Logs de acesso podem ser configurados

### Backup
- Backup manual do banco SQLite
- Exportação de dados via relatórios
- Backup automático (futuro)

## 🤝 Contribuição

### Como contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

### Padrões de código
- Python: PEP 8
- HTML: Semântico e acessível
- CSS: BEM methodology
- JavaScript: ES6+

## 📞 Suporte

### Problemas conhecidos
- SQLite não suporta múltiplos usuários simultâneos
- Upload de arquivos não implementado
- Notificações por email não configuradas

### Soluções
- Use PostgreSQL para produção
- Implemente sistema de upload
- Configure SMTP para emails

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🙏 Agradecimentos

- **MDA Wiki** (https://mda.wiki.br/) - Referência para especialidades
- **Bootstrap** - Framework CSS
- **Font Awesome** - Ícones
- **Flask** - Framework web Python

---

**Desenvolvido com ❤️ para os clubes de desbravadores**

*Sistema em constante evolução - contribuições são bem-vindas!*
