# importação de dependencias
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory,send_file,jsonify
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
import time
from datetime import date, timedelta
from gerenciadorImoveis import app, db
app.app_context().push()
db.create_all()
from sqlalchemy import func
from models import tb_user,\
    tb_usertype,\
    tb_clientes,\
    tb_terreno,\
    tb_terreno_arquivo,\
    tb_lote,\
    tb_lote_arquivo,\
    tb_venda
from helpers import \
    frm_pesquisa, \
    frm_editar_senha,\
    frm_editar_usuario,\
    frm_visualizar_usuario, \
    frm_visualizar_tipousuario,\
    frm_editar_tipousuario,\
    frm_visualizar_cliente,\
    frm_editar_cliente,\
    frm_editar_terreno,\
    frm_visualizar_terreno,\
    frm_editar_lote,\
    frm_visualizar_lote,\
    frm_editar_lote_arquivo,\
    frm_editar_terreno_arquivo,\
    frm_editar_venda,\
    frm_visualizar_venda

# ITENS POR PÁGINA
from config import ROWS_PER_PAGE, CHAVE
from flask_bcrypt import generate_password_hash, Bcrypt, check_password_hash

import string
import random
import numbers
import os

##################################################################################################################################
#GERAL
##################################################################################################################################


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: index
#FUNÇÃO: mostrar pagina principal
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))        
    return render_template('index.html', titulo='Bem vindos')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: logout
#FUNÇÃO: remover seção usuário
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso','success')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: login
#FUNÇÃO: iniciar seção do usuário
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: autenticar
#FUNÇÃO: autenticar
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/autenticar', methods = ['GET', 'POST'])
def autenticar():
    usuario = tb_user.query.filter_by(login_user=request.form['usuario']).first()
    senha = check_password_hash(usuario.password_user,request.form['senha'])
    if usuario:
        if senha:
            session['usuario_logado'] = usuario.login_user
            session['nomeusuario_logado'] = usuario.name_user
            session['tipousuario_logado'] = usuario.cod_usertype
            session['coduser_logado'] = usuario.cod_user
            flash(usuario.name_user + ' Usuário logado com sucesso','success')
            #return redirect('/')
            return redirect('/')
        else:
            flash('Verifique usuário e senha', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso','success')
        return redirect(url_for('login'))

##################################################################################################################################
#USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: usuario
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/usuario', methods=['POST','GET'])
def usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('usuario')))        
    form = frm_pesquisa()
    page = request.args.get('page', 1, type=int)
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data

    if pesquisa == "" or pesquisa == None:    
        usuarios = tb_user.query\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    else:
        usuarios = tb_user.query\
        .filter(tb_user.name_user.ilike(f'%{pesquisa}%'))\
        .join(tb_usertype, tb_usertype.cod_usertype==tb_user.cod_usertype)\
        .add_columns(tb_user.login_user, tb_user.cod_user, tb_user.name_user, tb_user.status_user, tb_usertype.desc_usertype)\
        .order_by(tb_user.name_user)\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)


    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoUsuario
#FUNÇÃO: formulário inclusão
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoUsuario')
def novoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoUsuario')))     
    form = frm_editar_usuario()
    return render_template('novoUsuario.html', titulo='Novo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuario
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarUsuario', methods=['POST',])
def criarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('criarUsuario')))      
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoUsuario'))
    nome  = form.nome.data
    status = form.status.data
    login = form.login.data
    tipousuario = form.tipousuario.data
    email = form.email.data
    #criptografar senha
    senha = generate_password_hash("teste@12345").decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('index')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso','success')
    return redirect(url_for('usuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarUsuarioexterno - NÃO DISPONIVEL NESTA VERSAO
#FUNÇÃO: formulário de inclusão
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/criarUsuarioexterno', methods=['POST',])
def criarUsuarioexterno():    
    nome  = request.form['nome']
    status = 0
    email = request.form['email']
    localarroba = email.find("@")
    login = email[0:localarroba]
    tipousuario = 2
    #criptografar senha
    senha = generate_password_hash(request.form['senha']).decode('utf-8')
    usuario = tb_user.query.filter_by(name_user=nome).first()
    if usuario:
        flash ('Usuário já existe','danger')
        return redirect(url_for('login')) 
    novoUsuario = tb_user(name_user=nome, status_user=status, login_user=login, cod_usertype=tipousuario, password_user=senha, email_user=email)
    db.session.add(novoUsuario)
    db.session.commit()
    flash('Usuário criado com sucesso, favor logar com ele','success')
    return redirect(url_for('login'))  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarUsuario
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarUsuario/<int:id>')
def visualizarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_visualizar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('visualizarUsuario.html', titulo='Visualizar Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarUsuario
#FUNÇÃO: formulario de edição
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/editarUsuario/<int:id>')
def editarUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarUsuario/<int:id>')))  
    usuario = tb_user.query.filter_by(cod_user=id).first()
    form = frm_editar_usuario()
    form.nome.data = usuario.name_user
    form.status.data = usuario.status_user
    form.login.data = usuario.login_user
    form.tipousuario.data = usuario.cod_usertype
    form.email.data = usuario.email_user
    return render_template('editarUsuario.html', titulo='Editar Usuário', id=id, form=form)    
       
#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarUsuario
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarUsuario', methods=['POST',])
def atualizarUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_usuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('atualizarUsuario'))
    id = request.form['id']
    usuario = tb_user.query.filter_by(cod_user=request.form['id']).first()
    usuario.name_user = form.nome.data
    usuario.status_user = form.status.data
    usuario.login_user = form.login.data
    usuario.cod_uertype = form.tipousuario.data
    db.session.add(usuario)
    db.session.commit()
    flash('Usuário alterado com sucesso','success')
    return redirect(url_for('visualizarUsuario', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarSenhaUsuario
#FUNÇÃO: formulario de edição
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarSenhaUsuario/')
def editarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarUsuario')))    
    form = frm_editar_senha()
    return render_template('trocarsenha.html', titulo='Trocar Senha', id=id, form=form)  

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: trocarSenhaUsuario
#FUNÇÃO: alteração no banco de dados
#PODE ACESSAR: todos
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/trocarSenhaUsuario', methods=['POST',])
def trocarSenhaUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarUsuario')))          
    form = frm_editar_senha(request.form)
    if form.validate_on_submit():
        id = session['coduser_logado']
        usuario = tb_user.query.filter_by(cod_user=id).first()
        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario'))

        if form.senhaatual.data != usuario.password_user:
            flash('senha atual incorreta','danger')
            return redirect(url_for('editarSenhaUsuario')) 

        if form.novasenha1.data != form.novasenha2.data:
            flash('novas senhas não coincidem','danger')
            return redirect(url_for('editarSenhaUsuario')) 
        usuario.password_user = generate_password_hash(form.novasenha1.data).decode('utf-8')
        db.session.add(usuario)
        db.session.commit()
        flash('senha alterada com sucesso!','success')
    else:
        flash('senha não alterada!','danger')
    return redirect(url_for('editarSenhaUsuario')) 

##################################################################################################################################
#TIPO DE USUARIOS
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: tipousuario
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/tipousuario', methods=['POST','GET'])
def tipousuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('tipousuario')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        tiposusuario = tb_usertype.query.order_by(tb_usertype.desc_usertype)\
        .filter(tb_usertype.desc_usertype.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('tipousuarios.html', titulo='Tipo Usuário', tiposusuario=tiposusuario, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTipoUsuario
#FUNÇÃO: formulario de inclusão
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTipoUsuario')
def novoTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTipoUsuario'))) 
    form = frm_editar_tipousuario()
    return render_template('novoTipoUsuario.html', titulo='Novo Tipo Usuário', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTipoUsuario
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTipoUsuario', methods=['POST',])
def criarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTipoUsuario')))     
    form = frm_editar_tipousuario(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarTipoUsuario'))
    desc  = form.descricao.data
    status = form.status.data
    tipousuario = tb_usertype.query.filter_by(desc_usertype=desc).first()
    if tipousuario:
        flash ('Tipo Usuário já existe','danger')
        return redirect(url_for('tipousuario')) 
    novoTipoUsuario = tb_usertype(desc_usertype=desc, status_usertype=status)
    flash('Tipo de usuário criado com sucesso!','success')
    db.session.add(novoTipoUsuario)
    db.session.commit()
    return redirect(url_for('tipousuario'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTipoUsuario
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTipoUsuario/<int:id>')
def visualizarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_visualizar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('visualizarTipoUsuario.html', titulo='Visualizar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTipoUsuario
##FUNÇÃO: formulário de edição
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTipoUsuario/<int:id>')
def editarTipoUsuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTipoUsuario')))  
    tipousuario = tb_usertype.query.filter_by(cod_usertype=id).first()
    form = frm_editar_tipousuario()
    form.descricao.data = tipousuario.desc_usertype
    form.status.data = tipousuario.status_usertype
    return render_template('editarTipoUsuario.html', titulo='Editar Tipo Usuário', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTipoUsuario
#FUNÇÃO: alterar informações no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTipoUsuario', methods=['POST',])
def atualizarTipoUsuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTipoUsuario')))      
    form = frm_editar_tipousuario(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        tipousuario = tb_usertype.query.filter_by(cod_usertype=request.form['id']).first()
        tipousuario.desc_usertype = form.descricao.data
        tipousuario.status_usertype = form.status.data
        db.session.add(tipousuario)
        db.session.commit()
        flash('Tipo de usuário atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTipoUsuario', id=request.form['id']))


##################################################################################################################################
#CLIENTE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: cliente
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/cliente', methods=['POST','GET'])
def cliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('cliente')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        clientes = tb_clientes.query.order_by(tb_clientes.nomerazao_cliente)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        clientes = tb_clientes.query.order_by(tb_clientes.nomerazao_cliente)\
        .filter(tb_clientes.nomerazao_cliente.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('cliente.html', titulo='Cliente', clientes=clientes, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoCliente
#FUNÇÃO: formulario de inclusão
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoCliente')
def novoCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoCliente'))) 
    form = frm_editar_cliente()
    return render_template('novoCliente.html', titulo='Novo Cliente', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarCliente
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarCliente', methods=['POST',])
def criarCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarCliente')))     
    form = frm_editar_cliente(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('criarCliente'))
    nomerazao_cliente  = form.nomerazao_cliente.data
    nomefantasia_cliente = form.nomefantasia_cliente.data
    end_cliente = form.end_cliente.data
    numend_cliente = form.numend_cliente.data
    bairro_cliente = form.bairro_cliente.data
    cidade_cliente = form.cidade_cliente.data
    uf_cliente = form.uf_cliente.data
    complemento_cliente = form.complemento_cliente.data
    cnpj_cliente = form.nomerazao_cliente.data
    status = form.status.data
    cliente = tb_clientes.query.filter_by(cnpj_cliente=cnpj_cliente).first()
    if cliente:
        flash ('Patrocinador já existe','danger')
        return redirect(url_for('cliente')) 
    novoCliente = tb_clientes(nomerazao_cliente=nomerazao_cliente,\
                            nomefantasia_cliente = nomefantasia_cliente,\
                            end_cliente = end_cliente,\
                            numend_cliente = numend_cliente,\
                            bairro_cliente = bairro_cliente,\
                            cidade_cliente = cidade_cliente,\
                            uf_cliente = uf_cliente,\
                            complemento_cliente = complemento_cliente,\
                            cnpj_cliente = cnpj_cliente,\
                            status_cliente=status)
    flash('Cliente criado com sucesso!','success')
    db.session.add(novoCliente)
    db.session.commit()
    return redirect(url_for('cliente'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarCliente
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarCliente/<int:id>')
def visualizarCliente(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarCliente')))  
    cliente = tb_clientes.query.filter_by(cod_cliente=id).first()
    form = frm_visualizar_cliente()
    form.nomerazao_cliente.data = cliente.nomerazao_cliente
    form.nomefantasia_cliente.data = cliente.nomefantasia_cliente
    form.end_cliente.data = cliente.end_cliente
    form.numend_cliente.data = cliente.numend_cliente
    form.bairro_cliente.data = cliente.bairro_cliente
    form.cidade_cliente.data = cliente.cidade_cliente
    form.uf_cliente.data = cliente.uf_cliente
    form.complemento_cliente.data = cliente.complemento_cliente
    form.cnpj_cliente.data = cliente.cnpj_cliente
    form.status.data = cliente.status_cliente
    return render_template('visualizarCliente.html', titulo='Visualizar Cliente', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarCliente
##FUNÇÃO: formulário de edição
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarCliente/<int:id>')
def editarCliente(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarCliente')))  
    cliente = tb_clientes.query.filter_by(cod_cliente=id).first()
    form = frm_editar_cliente()
    form.nomerazao_cliente.data = cliente.nomerazao_cliente
    form.nomefantasia_cliente.data = cliente.nomefantasia_cliente
    form.end_cliente.data = cliente.end_cliente
    form.numend_cliente.data = cliente.numend_cliente
    form.bairro_cliente.data = cliente.bairro_cliente
    form.cidade_cliente.data = cliente.cidade_cliente
    form.uf_cliente.data = cliente.uf_cliente
    form.complemento_cliente.data = cliente.complemento_cliente
    form.cnpj_cliente.data = cliente.cnpj_cliente
    form.status.data = cliente.status_cliente
    return render_template('editarCliente.html', titulo='Editar Cliente', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarCliente
#FUNÇÃO: alterar informações no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarCliente', methods=['POST',])
def atualizarCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarCliente')))      
    form = frm_editar_cliente(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        cliente = tb_clientes.query.filter_by(cod_cliente=request.form['id']).first()
        cliente.nomerazao_cliente = form.nomerazao_cliente.data
        cliente.nomefantasia_cliente = form.nomefantasia_cliente.data
        cliente.end_cliente = form.end_cliente.data
        cliente.numend_cliente = form.numend_cliente.data
        cliente.bairro_cliente = form.bairro_cliente.data
        cliente.cidade_cliente = form.cidade_cliente.data
        cliente.uf_cliente = form.uf_cliente.data
        cliente.complemento_cliente = form.complemento_cliente.data
        cliente.cnpj_cliente = form.cnpj_cliente.data
        cliente.status_cliente = form.status.data
        db.session.add(cliente)
        db.session.commit()
        flash('Patrocinador atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarCliente', id=request.form['id']))


##################################################################################################################################
#TERRENO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: terreno
#FUNÇÃO: listar
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/terreno', methods=['POST','GET'])
def terreno():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('cliente')))         
    page = request.args.get('page', 1, type=int)
    form = frm_pesquisa()   
    pesquisa = form.pesquisa.data
    if pesquisa == "":
        pesquisa = form.pesquisa_responsiva.data
    
    if pesquisa == "" or pesquisa == None:     
        terrenos = tb_terreno.query.order_by(tb_terreno.nome_terreno)\
        .paginate(page=page, per_page=ROWS_PER_PAGE , error_out=False)
    else:
        terrenos = tb_terreno.query.order_by(tb_clientes.nome_terreno)\
        .filter(tb_terreno.nome_terreno.ilike(f'%{pesquisa}%'))\
        .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)        
    return render_template('terreno.html', titulo='Terrenos', terrenos=terrenos, form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTerreno
#FUNÇÃO: formulario de inclusão
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoTerreno')
def novoTerreno():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoTerreno'))) 
    form = frm_editar_terreno()
    return render_template('novoTerreno.html', titulo='Novo Terreno', form=form)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarTerreno
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarTerreno', methods=['POST',])
def criarTerreno():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTerreno')))     
    form = frm_editar_terreno(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoTerreno'))
    nome_terreno  = form.nome_terreno.data
    end_terreno = form.end_terreno.data
    num_terreno = form.num_terreno.data
    bairro_terreno = form.bairro_terreno.data
    cidade_terreno = form.cidade_terreno.data
    uf_terreno = form.uf_terreno.data
    matricula_terreno = form.matricula_terreno.data
    status_terreno = form.status_terreno.data

    terreno = tb_terreno.query.filter_by(matricula_terreno=matricula_terreno).first()
    if terreno:
        flash ('Terreno já existe','danger')
        return redirect(url_for('terreno')) 
    novoTerreno = tb_terreno(nome_terreno=nome_terreno,\
                            end_terreno = end_terreno,\
                            num_terreno = num_terreno,\
                            bairro_terreno = bairro_terreno,\
                            cidade_terreno = cidade_terreno,\
                            uf_terreno = uf_terreno,\
                            matricula_terreno = matricula_terreno,\
                            status_terreno=status_terreno)
    flash('Terreno criado com sucesso!','success')
    db.session.add(novoTerreno)
    db.session.commit()
    return redirect(url_for('terreno'))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarTerreno
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarTerreno/<int:id>')
def visualizarTerreno(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarTerreno')))  
    terreno = tb_terreno.query.filter_by(cod_terreno=id).first()

    terreno_arquivos = tb_terreno_arquivo.query.filter_by(cod_terreno=id).all()

    lotes = tb_lote.query.order_by(tb_lote.cod_lote)\
        .filter(tb_lote.cod_terreno == id)

    form = frm_visualizar_terreno()
    form.nome_terreno.data = terreno.nome_terreno
    form.end_terreno.data = terreno.end_terreno
    form.num_terreno.data = terreno.num_terreno
    form.bairro_terreno.data = terreno.bairro_terreno
    form.cidade_terreno.data = terreno.cidade_terreno
    form.uf_terreno.data = terreno.uf_terreno
    form.matricula_terreno.data = terreno.matricula_terreno
    form.status_terreno.data = terreno.status_terreno
    return render_template('visualizarTerreno.html', titulo='Visualizar Terreno', id=id, form=form, terreno_arquivos=terreno_arquivos, lotes=lotes)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarTerreno
##FUNÇÃO: formulário de edição
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarTerreno/<int:id>')
def editarTerreno(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarTerreno')))  
    terreno = tb_terreno.query.filter_by(cod_terreno=id).first()
    form = frm_editar_terreno()
    form.nome_terreno.data = terreno.nome_terreno
    form.end_terreno.data = terreno.end_terreno
    form.num_terreno.data = terreno.num_terreno
    form.bairro_terreno.data = terreno.bairro_terreno
    form.cidade_terreno.data = terreno.cidade_terreno
    form.uf_terreno.data = terreno.uf_terreno
    form.matricula_terreno.data = terreno.matricula_terreno
    form.status_terreno.data = terreno.status_status_terrenocliente
    return render_template('editarTerreno.html', titulo='Editar Terreno', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarTerreno
#FUNÇÃO: alterar informações no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarTerreno', methods=['POST',])
def atualizarTerreno():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarTerreno')))      
    form = frm_editar_terreno(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        terreno = tb_terreno.query.filter_by(cod_terreno=id).first()
        terreno.nome_terreno = form.nome_terreno.data
        terreno.end_terreno = form.end_terreno.data
        terreno.num_terreno = form.num_terreno.data
        terreno.bairro_terreno = form.bairro_terreno.data
        terreno.cidade_terreno = form.cidade_terreno.data
        terreno.uf_terreno = form.uf_terreno.data
        terreno.matricula_terreno = form.matricula_terreno.data
        terreno.complemento_cliente = form.complemento_cliente.data
        terreno.status_terreno = form.status_terreno.data
        db.session.add(terreno)
        db.session.commit()
        flash('Terreno atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarTerreno', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoTerrenoArquivo
#FUNÇÃO: inclusão de arquivos banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoTerrenoArquivo/<int:id>')
def novoTerrenoArquivo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoSolicitacaoFoto'))) 
    form = frm_editar_terreno_arquivo()
    return render_template('novoTerrenoArquivo.html', titulo='Inserir Arquivo', form=form, id=id)

@app.route('/terreno_arquivo/<int:id>', methods=['POST'])
def terreno_arquivo(id):
    arquivo = request.files['arquivo_terreno_arquivo']
    nome_arquivo = secure_filename(arquivo.filename)
    nome_base, extensao = os.path.splitext(nome_arquivo)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    nome_unico = f"{nome_base}_{timestamp}{extensao}"
    caminho_arquivo = os.path.join(app.config['UPLOAD_PATH'], nome_unico)
    arquivo.save(caminho_arquivo)

    flash('Arquivo carregado com sucesso!','success')
    novoTerrenoArquivo = tb_terreno_arquivo(cod_terreno=id,arquivo_terreno_arquivo=nome_unico)
    db.session.add(novoTerrenoArquivo)
    db.session.commit()
    return redirect(url_for('novoTerrenoArquivo',id=id))


@app.route('/excluirArquivo/<int:id>')
def excluirArquivo(id):
    arquivo = tb_terreno_arquivo.query.filter_by(cod_terreno_arquivo=id).first()
    idterreno = arquivo.cod_solicitacao
    caminho_arquivo = os.path.join(app.config['UPLOAD_PATH'], arquivo.arquivo_terreno_arquivo)
    try:
        os.remove(caminho_arquivo)
        msg = "Arquivo excluído com sucesso!"
    except Exception as e:
        msg = f"Ocorreu um erro ao excluir o arquivo: {e}"

    apagarArqvuio = tb_terreno_arquivo.query.filter_by(cod_terreno_arquivo=id).one()
    db.session.delete(apagarArqvuio)
    db.session.commit()

    flash('Arquivo apagado com sucesso!','success')
    return redirect(url_for('visualizarTerreno',id=idterreno))


##################################################################################################################################
#LOTE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoLote
#FUNÇÃO: formulario de inclusão
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/novoLote/<int:id>')
def novoLote(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoLote',id=id))) 
    form = frm_editar_lote()
    return render_template('novoLote.html', titulo='Novo Lote', form=form,id=id)

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: criarLote
#FUNÇÃO: inclusão no banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/criarLote', methods=['POST',])
def criarLote():
    id = request.form['id']
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('criarTerreno')))     
    form = frm_editar_lote(request.form)
    if not form.validate_on_submit():
        flash('Por favor, preencha todos os dados','danger')
        return redirect(url_for('novoTerreno'))
    valortotal_lote  = form.valortotal_lote.data
    matricula_lote = form.matricula_lote.data
    status_lote = form.status_lote.data

    lote = tb_lote.query.filter_by(matricula_lote=matricula_lote).first()
    if lote:
        flash ('Terreno já existe','danger')
        return redirect(url_for('terreno')) 
    novoLote = tb_lote(valortotal_lote=valortotal_lote,\
                            matricula_lote = matricula_lote,\
                            cod_terreno = id,\
                            status_lote=status_lote)
    flash('Lote criado com sucesso!','success')
    db.session.add(novoLote)
    db.session.commit()
    return redirect(url_for('visualizarTerreno',id=id))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: visualizarLote
#FUNÇÃO: formulario de visualização
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/visualizarLote/<int:id>')
def visualizarLote(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('visualizarLote')))  
    lote = tb_lote.query.filter_by(cod_lote=id).first()

    idterreno = lote.cod_terreno
    form = frm_visualizar_lote()
    form.valortotal_lote.data = lote.valortotal_lote
    form.matricula_lote.data = lote.matricula_lote
    form.status_lote.data = lote.status_lote
    return render_template('visualizarLote.html', titulo='Visualizar Lote', id=id, form=form, idterreno=idterreno)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: editarLote
##FUNÇÃO: formulário de edição
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/editarLote/<int:id>')
def editarLote(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('editarLote'))) 
    
    lote = tb_lote.query.filter_by(cod_lote=id).first()
    form = frm_editar_lote()
    form.valortotal_lote.data = lote.valortotal_lote
    form.matricula_lote.data = lote.matricula_lote
    form.status_lote.data = lote.status_lote
    return render_template('editarLote.html', titulo='Editar Lote', id=id, form=form)   

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: atualizarLote
#FUNÇÃO: alterar informações no banco de dados
#PODE ACESSAR: administrador
#---------------------------------------------------------------------------------------------------------------------------------
@app.route('/atualizarLote', methods=['POST',])
def atualizarLote():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('atualizarLote')))      
    form = frm_editar_lote(request.form)
    if form.validate_on_submit():
        id = request.form['id']
        lote = tb_lote.query.filter_by(cod_lote=id).first()
        lote.valortotal_lote = form.valortotal_lote.data
        lote.matricula_lote = form.matricula_lote.data
        lote.status_lote = form.status_lote.data
        db.session.add(lote)
        db.session.commit()
        flash('Lote atualizado com sucesso!','success')
    else:
        flash('Favor verificar os campos!','danger')
    return redirect(url_for('visualizarLote', id=request.form['id']))

#---------------------------------------------------------------------------------------------------------------------------------
#ROTA: novoLoteArquivo
#FUNÇÃO: inclusão de arquivos banco de dados
#PODE ACESSAR: administrador
#--------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/novoLoteArquivo/<int:id>')
def novoLoteArquivo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sessão expirou, favor logar novamente','danger')
        return redirect(url_for('login',proxima=url_for('novoSolicitacaoFoto'))) 
    form = frm_editar_terreno_arquivo()
    return render_template('novoLoteArquivo.html', titulo='Inserir arquivos', form=form, id=id)

@app.route('/lote_arquivo/<int:id>', methods=['POST'])
def lote_arquivo(id):
    arquivo = request.files['arquivo_lote_arquivo']
    nome_arquivo = secure_filename(arquivo.filename)
    nome_base, extensao = os.path.splitext(nome_arquivo)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    nome_unico = f"{nome_base}_{timestamp}{extensao}"
    caminho_arquivo = os.path.join(app.config['UPLOAD_PATH'], nome_unico)
    arquivo.save(caminho_arquivo)

    flash('Arquivo carregado com sucesso!','success')
    novoLoteArquivo = tb_lote_arquivo(cod_terreno=id,arquivo_terreno_arquivo=nome_unico)
    db.session.add(novoLoteArquivo)
    db.session.commit()
    return redirect(url_for('novoLoteArquivo',id=id))


@app.route('/excluirLoteArquivo/<int:id>')
def excluirLoteArquivo(id):
    arquivo = tb_lote_arquivo.query.filter_by(cod_lotearquivo=id).first()
    idlote = arquivo.cod_lotearquivo
    caminho_arquivo = os.path.join(app.config['UPLOAD_PATH'], arquivo.arquivo_lote_arquivo)
    try:
        os.remove(caminho_arquivo)
        msg = "Arquivo excluído com sucesso!"
    except Exception as e:
        msg = f"Ocorreu um erro ao excluir o arquivo: {e}"

    apagarArquivo = tb_lote_arquivo.query.filter_by(cod_lote_arquivo=id).one()
    db.session.delete(apagarArquivo)
    db.session.commit()

    flash('Arquivo apagado com sucesso!','success')
    return redirect(url_for('visualizarLote',id=idlote))