# Instruções de Instalação - Sistema de Desbravadores

## 🚀 Instalação Rápida

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema
```bash
python run.py
```

### 4. Acessar o Sistema
- Abra seu navegador em: `http://127.0.0.1:5000`
- **Login**: `admin`
- **Senha**: `admin123`
- ⚠️ **Altere a senha após o primeiro login!**

## 📋 Funcionalidades Disponíveis

### ✅ Implementadas
- ✅ Sistema de login seguro
- ✅ Dashboard com estatísticas
- ✅ Cadastro de desbravadores
- ✅ Controle de mensalidades
- ✅ Gestão financeira
- ✅ Relatórios básicos
- ✅ Interface responsiva
- ✅ Tema escuro moderno

### 🔄 Em Desenvolvimento
- 🔄 Exportação de relatórios (PDF/Excel)
- 🔄 Sistema de eventos
- 🔄 Notificações por email
- 🔄 Backup automático

## 🎨 Personalização

### Cores do Tema
- **Azul Principal**: #1e3a8a
- **Amarelo Secundário**: #fbbf24
- **Preto Base**: #1a1a1a

### Modificar Cores
Edite o arquivo `app/static/css/style.css` e altere as variáveis CSS:
```css
:root {
    --primary-color: #sua-cor-aqui;
    --secondary-color: #sua-cor-aqui;
}
```

## 🔧 Configurações Avançadas

### Banco de Dados
Por padrão, o sistema usa SQLite. Para produção, configure PostgreSQL:
```python
# No arquivo app/__init__.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
```

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///desbravadores.db
FLASK_DEBUG=True
```

## 📱 Responsividade

O sistema funciona em:
- 💻 Desktop (1200px+)
- 📱 Tablet (768px - 1199px)
- 📱 Mobile (até 767px)

## 🚀 Deploy em Produção

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Usando Nginx (recomendado)
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Segurança

### Recomendações
1. Altere a senha padrão do admin
2. Use HTTPS em produção
3. Configure backup regular
4. Mantenha o sistema atualizado

### Backup
```bash
# Backup do banco SQLite
cp desbravadores.db backup_$(date +%Y%m%d).db
```

## 🆘 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de Banco de Dados
```bash
# Remover banco corrompido
rm desbravadores.db
python run.py  # Recriará automaticamente
```

### Erro de Porta em Uso
```bash
# Alterar porta no arquivo run.py
app.run(port=5001)
```

## 📞 Suporte

### Logs de Erro
Os erros são salvos automaticamente. Verifique:
- Console do terminal
- Arquivo de log (se configurado)

### Contato
- 📧 Email: suporte@desbravadores.com
- 📱 WhatsApp: (11) 99999-9999
- 🌐 Site: https://sistema-desbravadores.com

---

**Sistema desenvolvido com ❤️ para os clubes de desbravadores**
