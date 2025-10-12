from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Desbravador, Evento
from app import db
from datetime import datetime, date
import calendar

desbravador_bp = Blueprint('desbravador', __name__)

@desbravador_bp.route('/desbravador/dashboard')
@login_required
def dashboard():
    """Dashboard para desbravadores com acesso restrito"""
    # Verificar se é um desbravador logado
    if not isinstance(current_user, Desbravador):
        flash('Acesso negado! Esta área é apenas para desbravadores.', 'error')
        return redirect(url_for('auth.login'))
    
    # Obter eventos do mês atual
    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Eventos do mês atual
    eventos_mes = Evento.query.filter(
        Evento.data_inicio >= datetime(ano_atual, mes_atual, 1),
        Evento.data_inicio < datetime(ano_atual, mes_atual + 1, 1) if mes_atual < 12 else datetime(ano_atual + 1, 1, 1),
        Evento.ativo == True
    ).order_by(Evento.data_inicio).all()
    
    # Próximos eventos (próximos 30 dias)
    proximos_eventos = Evento.query.filter(
        Evento.data_inicio >= hoje,
        Evento.data_inicio <= datetime(ano_atual, mes_atual + 1, hoje.day) if mes_atual < 12 else datetime(ano_atual + 1, 1, hoje.day),
        Evento.ativo == True
    ).order_by(Evento.data_inicio).limit(5).all()
    
    # Calendário do mês atual
    cal = calendar.monthcalendar(ano_atual, mes_atual)
    
    # Mapear eventos por dia
    eventos_por_dia = {}
    for evento in eventos_mes:
        dia = evento.data_inicio.day
        if dia not in eventos_por_dia:
            eventos_por_dia[dia] = []
        eventos_por_dia[dia].append(evento)
    
    return render_template('desbravador/dashboard.html', 
                         desbravador=current_user,
                         eventos_mes=eventos_mes,
                         proximos_eventos=proximos_eventos,
                         calendario=cal,
                         eventos_por_dia=eventos_por_dia,
                         mes_atual=mes_atual,
                         ano_atual=ano_atual,
                         hoje=hoje)

@desbravador_bp.route('/desbravador/calendario')
@login_required
def calendario():
    """Página de calendário completo para desbravadores"""
    # Verificar se é um desbravador logado
    if not isinstance(current_user, Desbravador):
        flash('Acesso negado! Esta área é apenas para desbravadores.', 'error')
        return redirect(url_for('auth.login'))
    
    # Obter mês e ano da URL ou usar atual
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    # Validar mês e ano
    if mes < 1 or mes > 12:
        mes = datetime.now().month
    if ano < 2020 or ano > 2030:
        ano = datetime.now().year
    
    # Eventos do mês
    eventos_mes = Evento.query.filter(
        Evento.data_inicio >= datetime(ano, mes, 1),
        Evento.data_inicio < datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1),
        Evento.ativo == True
    ).order_by(Evento.data_inicio).all()
    
    # Calendário do mês
    cal = calendar.monthcalendar(ano, mes)
    
    # Mapear eventos por dia
    eventos_por_dia = {}
    for evento in eventos_mes:
        dia = evento.data_inicio.day
        if dia not in eventos_por_dia:
            eventos_por_dia[dia] = []
        eventos_por_dia[dia].append(evento)
    
    # Navegação de mês
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1
    mes_proximo = mes + 1 if mes < 12 else 1
    ano_proximo = ano if mes < 12 else ano + 1
    
    return render_template('desbravador/calendario.html',
                         desbravador=current_user,
                         eventos_mes=eventos_mes,
                         calendario=cal,
                         eventos_por_dia=eventos_por_dia,
                         mes_atual=mes,
                         ano_atual=ano,
                         mes_anterior=mes_anterior,
                         ano_anterior=ano_anterior,
                         mes_proximo=mes_proximo,
                         ano_proximo=ano_proximo,
                         hoje=datetime.now())

@desbravador_bp.route('/desbravador/perfil')
@login_required
def perfil():
    """Perfil do desbravador"""
    # Verificar se é um desbravador logado
    if not isinstance(current_user, Desbravador):
        flash('Acesso negado! Esta área é apenas para desbravadores.', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('desbravador/perfil.html', desbravador=current_user)

