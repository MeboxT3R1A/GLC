from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models import Desbravador, Mensalidade, Transacao
from app import db
from datetime import datetime, date
import calendar

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/')
@login_required
def index():
    """Página inicial de relatórios"""
    return render_template('relatorios/index.html')

@relatorios_bp.route('/mensalidades')
@login_required
def relatorio_mensalidades():
    """Relatório de mensalidades"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    mensalidades = Mensalidade.query.filter_by(
        mes_referencia=mes,
        ano_referencia=ano
    ).join(Desbravador).order_by(Desbravador.nome).all()
    
    # Estatísticas
    total_desbravadores = len(mensalidades)
    pagas = len([m for m in mensalidades if m.status == 'pago'])
    pendentes = len([m for m in mensalidades if m.status == 'pendente'])
    atrasadas = len([m for m in mensalidades if m.status == 'atrasado'])
    
    valor_total = sum(m.valor for m in mensalidades)
    valor_pago = sum(m.valor for m in mensalidades if m.status == 'pago')
    valor_pendente = sum(m.valor for m in mensalidades if m.status == 'pendente')
    
    stats = {
        'total_desbravadores': total_desbravadores,
        'pagas': pagas,
        'pendentes': pendentes,
        'atrasadas': atrasadas,
        'valor_total': valor_total,
        'valor_pago': valor_pago,
        'valor_pendente': valor_pendente,
        'percentual_pago': (pagas / total_desbravadores * 100) if total_desbravadores > 0 else 0
    }
    
    return render_template('relatorios/mensalidades.html',
                         mensalidades=mensalidades,
                         stats=stats,
                         mes=mes,
                         ano=ano)

@relatorios_bp.route('/fluxo-caixa')
@login_required
def relatorio_fluxo_caixa():
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
    
    # Separar receitas e despesas
    receitas = [t for t in transacoes if t.tipo == 'receita']
    despesas = [t for t in transacoes if t.tipo == 'despesa']
    
    total_receitas = sum(t.valor for t in receitas)
    total_despesas = sum(t.valor for t in despesas)
    saldo = total_receitas - total_despesas
    
    return render_template('relatorios/fluxo_caixa.html',
                         transacoes=transacoes,
                         receitas=receitas,
                         despesas=despesas,
                         total_receitas=total_receitas,
                         total_despesas=total_despesas,
                         saldo=saldo,
                         mes=mes,
                         ano=ano)

@relatorios_bp.route('/patrimonio')
@login_required
def relatorio_patrimonio():
    """Relatório de patrimônio"""
    # Buscar todas as transações
    receitas = Transacao.query.filter_by(tipo='receita').all()
    despesas = Transacao.query.filter_by(tipo='despesa').all()
    
    total_receitas = sum(t.valor for t in receitas)
    total_despesas = sum(t.valor for t in despesas)
    patrimonio_atual = total_receitas - total_despesas
    
    # Receitas por categoria
    receitas_por_categoria = {}
    for transacao in receitas:
        categoria = transacao.categoria
        if categoria not in receitas_por_categoria:
            receitas_por_categoria[categoria] = 0
        receitas_por_categoria[categoria] += transacao.valor
    
    # Despesas por categoria
    despesas_por_categoria = {}
    for transacao in despesas:
        categoria = transacao.categoria
        if categoria not in despesas_por_categoria:
            despesas_por_categoria[categoria] = 0
        despesas_por_categoria[categoria] += transacao.valor
    
    return render_template('relatorios/patrimonio.html',
                         total_receitas=total_receitas,
                         total_despesas=total_despesas,
                         patrimonio_atual=patrimonio_atual,
                         receitas_por_categoria=receitas_por_categoria,
                         despesas_por_categoria=despesas_por_categoria)

@relatorios_bp.route('/desbravadores')
@login_required
def relatorio_desbravadores():
    """Relatório de desbravadores"""
    # Estatísticas gerais
    total_desbravadores = Desbravador.query.filter_by(ativo=True).count()
    
    # Por unidade
    unidades = db.session.query(
        Desbravador.unidade,
        db.func.count(Desbravador.id)
    ).filter_by(ativo=True).group_by(Desbravador.unidade).all()
    
    # Por classe
    classes = db.session.query(
        Desbravador.classe,
        db.func.count(Desbravador.id)
    ).filter_by(ativo=True).group_by(Desbravador.classe).all()
    
    # Por faixa etária
    faixas_etarias = {
        '6-9 anos': Desbravador.query.filter(Desbravador.idade >= 6, Desbravador.idade <= 9, Desbravador.ativo == True).count(),
        '10-12 anos': Desbravador.query.filter(Desbravador.idade >= 10, Desbravador.idade <= 12, Desbravador.ativo == True).count(),
        '13-15 anos': Desbravador.query.filter(Desbravador.idade >= 13, Desbravador.idade <= 15, Desbravador.ativo == True).count(),
        '16+ anos': Desbravador.query.filter(Desbravador.idade >= 16, Desbravador.ativo == True).count()
    }
    
    return render_template('relatorios/desbravadores.html',
                         total_desbravadores=total_desbravadores,
                         unidades=unidades,
                         classes=classes,
                         faixas_etarias=faixas_etarias)

@relatorios_bp.route('/exportar/<tipo>')
@login_required
def exportar_relatorio(tipo):
    """Exportar relatório em formato específico"""
    # Implementar exportação para PDF, Excel, etc.
    flash('Funcionalidade de exportação em desenvolvimento!', 'info')
    return redirect(url_for('relatorios.index'))
