from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models import Desbravador, Mensalidade
from app import db
from datetime import datetime, date
import json

desbravadores_bp = Blueprint('desbravadores', __name__)

@desbravadores_bp.route('/')
@login_required
def listar():
    """Lista todos os desbravadores"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Desbravador.query.filter_by(ativo=True)
    
    if search:
        query = query.filter(Desbravador.nome.contains(search))
    
    desbravadores = query.order_by(Desbravador.nome).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('desbravadores/listar.html', 
                         desbravadores=desbravadores, 
                         search=search)

@desbravadores_bp.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    """Cadastro de novo desbravador"""
    if request.method == 'POST':
        try:
            # Processar especialidades
            especialidades = request.form.getlist('especialidades')
            
            # Converter data de nascimento
            data_nascimento_str = request.form['data_nascimento']
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            
            # Calcular idade
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            novo_desbravador = Desbravador(
                nome=request.form['nome'],
                idade=idade,
                data_nascimento=data_nascimento,
                unidade=request.form['unidade'],
                classe=request.form['classe'],
                especialidades=json.dumps(especialidades),
                telefone=request.form.get('telefone', ''),
                email=request.form.get('email', ''),
                endereco=request.form.get('endereco', ''),
                nome_responsavel=request.form.get('nome_responsavel', ''),
                telefone_responsavel=request.form.get('telefone_responsavel', '')
            )
            
            db.session.add(novo_desbravador)
            db.session.commit()
            
            flash('Desbravador cadastrado com sucesso!', 'success')
            return redirect(url_for('desbravadores.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar desbravador: {str(e)}', 'error')
    
    # Lista de especialidades disponíveis (baseada no site MDA)
    especialidades_disponiveis = [
        'ADRA', 'Artes e Habilidades Manuais', 'Atividades Agrícolas',
        'Atividades Missionárias e Comunitárias', 'Atividades Profissionais',
        'Atividades Recreativas', 'Ciência e Saúde', 'Estudos da Natureza',
        'Habilidades Domésticas'
    ]
    
    unidades_disponiveis = [
        'Amigo', 'Companheiro', 'Pesquisador', 'Pioneiro', 
        'Excursionista', 'Guia', 'Líder', 'Líder Master', 'Líder Master Avançado'
    ]
    
    return render_template('desbravadores/cadastrar.html',
                         especialidades=especialidades_disponiveis,
                         unidades=unidades_disponiveis)

@desbravadores_bp.route('/<int:id>')
@login_required
def visualizar(id):
    """Visualizar detalhes de um desbravador"""
    desbravador = Desbravador.query.get_or_404(id)
    
    # Carregar especialidades
    especialidades = json.loads(desbravador.especialidades) if desbravador.especialidades else []
    
    # Carregar mensalidades
    mensalidades = Mensalidade.query.filter_by(desbravador_id=id).order_by(
        Mensalidade.ano_referencia.desc(), 
        Mensalidade.mes_referencia.desc()
    ).all()
    
    return render_template('desbravadores/visualizar.html',
                         desbravador=desbravador,
                         especialidades=especialidades,
                         mensalidades=mensalidades)

@desbravadores_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar dados de um desbravador"""
    desbravador = Desbravador.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Processar especialidades
            especialidades = request.form.getlist('especialidades')
            
            # Converter data de nascimento
            data_nascimento_str = request.form['data_nascimento']
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            
            # Calcular idade
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            desbravador.nome = request.form['nome']
            desbravador.idade = idade
            desbravador.data_nascimento = data_nascimento
            desbravador.unidade = request.form['unidade']
            desbravador.classe = request.form['classe']
            desbravador.especialidades = json.dumps(especialidades)
            desbravador.telefone = request.form.get('telefone', '')
            desbravador.email = request.form.get('email', '')
            desbravador.endereco = request.form.get('endereco', '')
            desbravador.nome_responsavel = request.form.get('nome_responsavel', '')
            desbravador.telefone_responsavel = request.form.get('telefone_responsavel', '')
            
            db.session.commit()
            
            flash('Desbravador atualizado com sucesso!', 'success')
            return redirect(url_for('desbravadores.visualizar', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar desbravador: {str(e)}', 'error')
    
    # Carregar especialidades atuais
    especialidades_atuais = json.loads(desbravador.especialidades) if desbravador.especialidades else []
    
    especialidades_disponiveis = [
        'ADRA', 'Artes e Habilidades Manuais', 'Atividades Agrícolas',
        'Atividades Missionárias e Comunitárias', 'Atividades Profissionais',
        'Atividades Recreativas', 'Ciência e Saúde', 'Estudos da Natureza',
        'Habilidades Domésticas'
    ]
    
    unidades_disponiveis = [
        'Amigo', 'Companheiro', 'Pesquisador', 'Pioneiro', 
        'Excursionista', 'Guia', 'Líder', 'Líder Master', 'Líder Master Avançado'
    ]
    
    return render_template('desbravadores/editar.html',
                         desbravador=desbravador,
                         especialidades_disponiveis=especialidades_disponiveis,
                         especialidades_atuais=especialidades_atuais,
                         unidades=unidades_disponiveis)

@desbravadores_bp.route('/<int:id>/inativar', methods=['POST'])
@login_required
def inativar(id):
    """Inativar um desbravador"""
    desbravador = Desbravador.query.get_or_404(id)
    desbravador.ativo = False
    db.session.commit()
    
    flash('Desbravador inativado com sucesso!', 'success')
    return redirect(url_for('desbravadores.listar'))
