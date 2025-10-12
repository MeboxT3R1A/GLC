from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Desbravador, Mensalidade, Transacao
from app import db
from datetime import datetime, date

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login de usuários"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Rota para logout de usuários"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Rota para registro de novos usuários (apenas para setup inicial)"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nome_completo = request.form['nome_completo']
        cargo = request.form['cargo']
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe!', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('auth/register.html')
        
        # Criar novo usuário
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            nome_completo=nome_completo,
            cargo=cargo
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/desbravador-login', methods=['GET', 'POST'])
def desbravador_login():
    """Rota para login de desbravadores"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        desbravador = Desbravador.query.filter_by(username=username).first()
        
        if desbravador and desbravador.pode_fazer_login and check_password_hash(desbravador.password_hash, password):
            login_user(desbravador)
            flash(f'Bem-vindo, {desbravador.nome}!', 'success')
            return redirect(url_for('desbravador.dashboard'))
        else:
            flash('Usuário ou senha incorretos, ou login não autorizado!', 'error')
    
    return render_template('auth/desbravador_login.html')

@auth_bp.route('/desbravador-logout')
@login_required
def desbravador_logout():
    """Rota para logout de desbravadores"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.desbravador_login'))