from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models import Desbravador, Mensalidade, Transacao
from app import db
from datetime import datetime, date
import calendar

financeiro_bp = Blueprint('financeiro', __name__)

@financeiro_bp.route('/')
@login_required
def dashboard():
    """Dashboard financeiro"""
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    # Estatísticas do mês atual
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
    
    total_arrecadado = db.session.query(db.func.sum(Mensalidade.valor)).filter_by(
        mes_referencia=mes_atual,
        ano_referencia=ano_atual,
        status='pago'
    ).scalar() or 0
    
    # Transações recentes
    transacoes_recentes = Transacao.query.order_by(
        Transacao.data_transacao.desc()
    ).limit(10).all()
    
    stats = {
        'mensalidades_pagas': mensalidades_pagas,
        'mensalidades_pendentes': mensalidades_pendentes,
        'total_arrecadado': total_arrecadado,
        'mes_atual': calendar.month_name[mes_atual],
        'ano_atual': ano_atual
    }
    
    return render_template('financeiro/dashboard.html',
                         stats=stats,
                         transacoes_recentes=transacoes_recentes)

@financeiro_bp.route('/mensalidades')
@login_required
def mensalidades():
    """Controle de mensalidades"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    # Buscar mensalidades do mês/ano especificado
    mensalidades = Mensalidade.query.filter_by(
        mes_referencia=mes,
        ano_referencia=ano
    ).join(Desbravador).order_by(Desbravador.nome).all()
    
    # Se não existirem mensalidades para este mês, criar para todos os desbravadores ativos
    if not mensalidades:
        desbravadores_ativos = Desbravador.query.filter_by(ativo=True).all()
        for desbravador in desbravadores_ativos:
            mensalidade = Mensalidade(
                desbravador_id=desbravador.id,
                mes_referencia=mes,
                ano_referencia=ano,
                valor=50.0,  # Valor padrão da mensalidade
                status='pendente'
            )
            db.session.add(mensalidade)
        
        db.session.commit()
        
        # Recarregar mensalidades
        mensalidades = Mensalidade.query.filter_by(
            mes_referencia=mes,
            ano_referencia=ano
        ).join(Desbravador).order_by(Desbravador.nome).all()
    
    # Calcular totais
    total_pago = sum(m.valor for m in mensalidades if m.status == 'pago')
    total_pendente = sum(m.valor for m in mensalidades if m.status == 'pendente')
    total_geral = sum(m.valor for m in mensalidades)
    
    return render_template('financeiro/mensalidades.html',
                         mensalidades=mensalidades,
                         mes=mes,
                         ano=ano,
                         total_pago=total_pago,
                         total_pendente=total_pendente,
                         total_geral=total_geral)

@financeiro_bp.route('/mensalidades/<int:id>/pagar', methods=['POST'])
@login_required
def pagar_mensalidade(id):
    """Registrar pagamento de mensalidade"""
    mensalidade = Mensalidade.query.get_or_404(id)
    
    mensalidade.status = 'pago'
    mensalidade.data_pagamento = datetime.now()
    
    # Criar transação de receita
    transacao = Transacao(
        tipo='receita',
        categoria='mensalidade',
        descricao=f'Mensalidade - {mensalidade.desbravador.nome} - {mensalidade.mes_referencia}/{mensalidade.ano_referencia}',
        valor=mensalidade.valor,
        data_transacao=datetime.now()
    )
    
    db.session.add(transacao)
    db.session.commit()
    
    flash('Pagamento registrado com sucesso!', 'success')
    return redirect(url_for('financeiro.mensalidades'))

@financeiro_bp.route('/transacoes')
@login_required
def transacoes():
    """Lista de transações financeiras"""
    page = request.args.get('page', 1, type=int)
    tipo = request.args.get('tipo', '', type=str)
    
    query = Transacao.query
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    transacoes = query.order_by(Transacao.data_transacao.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('financeiro/transacoes.html',
                         transacoes=transacoes,
                         tipo=tipo)

@financeiro_bp.route('/transacoes/nova', methods=['GET', 'POST'])
@login_required
def nova_transacao():
    """Cadastrar nova transação"""
    if request.method == 'POST':
        try:
            transacao = Transacao(
                tipo=request.form['tipo'],
                categoria=request.form['categoria'],
                descricao=request.form['descricao'],
                valor=float(request.form['valor']),
                data_transacao=datetime.strptime(request.form['data_transacao'], '%Y-%m-%d'),
                observacoes=request.form.get('observacoes', '')
            )
            
            db.session.add(transacao)
            db.session.commit()
            
            flash('Transação cadastrada com sucesso!', 'success')
            return redirect(url_for('financeiro.transacoes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar transação: {str(e)}', 'error')
    
    categorias_receita = [
        'mensalidade', 'evento', 'doação', 'venda', 'outros'
    ]
    
    categorias_despesa = [
        'material', 'evento', 'manutenção', 'alimentação', 'transporte', 'outros'
    ]
    
    return render_template('financeiro/nova_transacao.html',
                         categorias_receita=categorias_receita,
                         categorias_despesa=categorias_despesa)

@financeiro_bp.route('/fluxo-caixa')
@login_required
def fluxo_caixa():
    """Relatório de fluxo de caixa"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    # Buscar transações do mês
    inicio_mes = datetime(ano, mes, 1)
    if mes == 12:
        fim_mes = datetime(ano + 1, 1, 1)
    else:
        fim_mes = datetime(ano, mes + 1, 1)
    
    transacoes = Transacao.query.filter(
        Transacao.data_transacao >= inicio_mes,
        Transacao.data_transacao < fim_mes
    ).order_by(Transacao.data_transacao).all()
    
    # Calcular saldo
    saldo_inicial = 0  # Implementar cálculo do saldo inicial
    saldo_atual = saldo_inicial
    
    for transacao in transacoes:
        if transacao.tipo == 'receita':
            saldo_atual += transacao.valor
        else:
            saldo_atual -= transacao.valor
    
    return render_template('financeiro/fluxo_caixa.html',
                         transacoes=transacoes,
                         mes=mes,
                         ano=ano,
                         saldo_inicial=saldo_inicial,
                         saldo_atual=saldo_atual)
