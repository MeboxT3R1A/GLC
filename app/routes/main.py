from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Desbravador, Mensalidade, Transacao, User
from app import db
from datetime import datetime, date
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial - redireciona para login se não autenticado"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do sistema"""
    # Estatísticas para o dashboard
    total_desbravadores = Desbravador.query.filter_by(ativo=True).count()
    
    # Mensalidades do mês atual
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    mensalidades_pagas = Mensalidade.query.filter_by(
        mes_referencia=mes_atual,
        ano_referencia=ano_atual,
        status='pago'
    ).count()
    
    mensalidades_pendentes = Mensalidade.query.filter_by(
        mes_referencia=mes_atual,
        ano_referencia=ano_atual,
        status='pendente'
    ).count()
    
    # Valor total arrecadado no mês
    total_arrecadado = db.session.query(db.func.sum(Mensalidade.valor)).filter_by(
        mes_referencia=mes_atual,
        ano_referencia=ano_atual,
        status='pago'
    ).scalar() or 0
    
    # Desbravadores recentes (últimos 5 cadastrados)
    desbravadores_recentes = Desbravador.query.filter_by(ativo=True).order_by(
        Desbravador.data_cadastro.desc()
    ).limit(5).all()
    
    # Mensalidades em atraso
    mensalidades_atrasadas = Mensalidade.query.filter(
        Mensalidade.status == 'atrasado'
    ).count()
    
    stats = {
        'total_desbravadores': total_desbravadores,
        'mensalidades_pagas': mensalidades_pagas,
        'mensalidades_pendentes': mensalidades_pendentes,
        'total_arrecadado': total_arrecadado,
        'mensalidades_atrasadas': mensalidades_atrasadas
    }
    
    return render_template('main/dashboard.html', 
                         stats=stats, 
                         desbravadores_recentes=desbravadores_recentes)

@main_bp.route('/profile')
@login_required
def profile():
    """Perfil do usuário logado"""
    return render_template('main/profile.html')

@main_bp.route('/settings')
@login_required
def settings():
    """Configurações do sistema"""
    return render_template('main/settings.html')
