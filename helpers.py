#importações
import os
from gerenciadorImoveis import app, db
from models import tb_user, tb_usertype, tb_cliente, tb_lote
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SubmitField,IntegerField, SelectField,PasswordField,DateField,EmailField,BooleanField,RadioField, TextAreaField, TimeField, TelField, DateTimeLocalField,FloatField, DecimalField,FileField

##################################################################################################################################
#PESQUISA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: pesquisa (geral)
#TIPO: edição
#TABELA: nenhuma
#---------------------------------------------------------------------------------------------------------------------------------
class frm_pesquisa(FlaskForm):
    pesquisa = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )
    pesquisa_responsiva = StringField('Pesquisa:', [validators.Length(min=1, max=50)],render_kw={"placeholder": "digite sua pesquisa"} )

##################################################################################################################################
#USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o nome do usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")])
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o login do usuário"})    
    tipousuario = SelectField('Situação:', coerce=int,  choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.order_by('desc_usertype')])
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "digite o email do usuário"})


#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: usuários
#TIPO: visualização
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_usuario(FlaskForm):
    nome = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0,"Ativo"),(1,"Inativo")], render_kw={'readonly': True})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    tipousuario = SelectField('Tipo:', coerce=int, choices=[(g.cod_usertype, g.desc_usertype) for g in tb_usertype.query.all()], render_kw={'readonly': True})
    email = EmailField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: trocar senha do usuário
#TIPO: edição
#TABELA: tb_user
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_senha(FlaskForm):
    senhaatual = PasswordField('Senha Atual:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a senha atual"})
    novasenha1 = PasswordField('Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a nova senha"})
    novasenha2 = PasswordField('Confirme Nova Senha:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite novamente a senha"})

##################################################################################################################################
#TIPO DE USUÁRIO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: edição
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a descrição do tipo de usuário"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])  

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: tipo de usuário
#TIPO: visualização
#TABELA: tb_usertype
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_tipousuario(FlaskForm):
    descricao = StringField('Descrição:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})

##################################################################################################################################
#CLIENTES
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: cliente
#TIPO: edição
#TABELA: tb_cliente
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_cliente(FlaskForm):
    nome_cliente = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome social do cliente"})
    end_cliente = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o endereço do cliente"})
    numend_cliente = StringField('Nº:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o número do endereço do cliente"})
    bairro_cliente = StringField('Bairro:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o bairro do cliente"})
    cidade_cliente = StringField('Cidade:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a cidade do cliente"})
    uf_cliente = StringField('Uf:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a uf cliente"})
    complemento_cliente = StringField('Complemento:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o complemento do endereço do cliente"})
    cpf_cliente = StringField('CPF:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o cpf do cliente"})
    fone_cliente = StringField('Telefone:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o cpf do cliente"})
    email_cliente = StringField('E-mail:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o cpf do cliente"})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')])

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: cliente
#TIPO: visualização
#TABELA: tb_cliente
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_cliente(FlaskForm):
    nome_cliente = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    end_cliente = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    numend_cliente = StringField('Nº:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    bairro_cliente = StringField('Bairro:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    cidade_cliente = StringField('Cidade:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    uf_cliente = StringField('Uf:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    complemento_cliente = StringField('Complemento:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    cpf_cliente = StringField('CPF:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    fone_cliente = StringField('Telefone:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    email_cliente = StringField('E-mail:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})   

##################################################################################################################################
#TERRENO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: terreno
#TIPO: edição
#TABELA: tb_terreno
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_terreno(FlaskForm):
    nome_terreno = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o nome do terreno"})
    end_terreno = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o endereço do terreno"})
    num_terreno = StringField('Nº:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o número do terreno"})
    bairro_terreno = StringField('Bairro:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o bairro do terreno"})
    cidade_terreno = StringField('Cidade:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o cidade do terreno"})
    uf_terreno = StringField('Uf:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o estado terreno"})
    matricula_terreno = StringField('Matricula:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o matrícula do terreno"})
    status_terreno = SelectField('Situação:', coerce=int, choices=[(0, 'A venda'),(1, 'Vendido'),(2, 'Suspenso')])

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: terreno
#TIPO: visualização
#TABELA: tb_terreno
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_terreno(FlaskForm):
    end_terreno = StringField('Endereço:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    nome_terreno = StringField('Nome:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    num_terreno = StringField('Nº:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    bairro_terreno = StringField('Bairro:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    cidade_terreno = StringField('Cidade:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    uf_terreno = StringField('Uf:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    matricula_terreno = StringField('Matricula:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status_terreno = SelectField('Situação:', coerce=int, choices=[(0, 'A venda'),(1, 'Vendido'),(2, 'Suspenso')], render_kw={'readonly': True})

##################################################################################################################################
#TERRENO / ARQUIVO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: terreno / arquivo
#TIPO: edição
#TABELA: tb_terreno_arquivo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_terreno_arquivo(FlaskForm):
    arquivo_terreno_arquivo = FileField('Arquivo:', [validators.DataRequired()], render_kw={"placeholder": "selecionar arquivo"})

##################################################################################################################################
#LOTE
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: lote
#TIPO: edição
#TABELA: tb_lote
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_lote(FlaskForm):
    valortotal_lote = StringField('Valor:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite o valor do lote"})
    matricula_lote = StringField('Matricula:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "digite a matricula do lote"})
    status_lote = SelectField('Situação:', coerce=int, choices=[(0, 'A Venda'),(1, 'Vendido')])

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: aditivo
#TIPO: visualização
#TABELA: tb_aditivos
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_lote(FlaskForm):
    valortotal_lote = StringField('Valor:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    matricula_lote = StringField('Matricula:', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'readonly': True})
    status_lote = SelectField('Situação:', coerce=int, choices=[(0, 'Ativo'),(1, 'Inativo')], render_kw={'readonly': True})

##################################################################################################################################
#LOTE / ARQUIVO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: lote / arquivo
#TIPO: edição
#TABELA: tb_lote_arquivo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_lote_arquivo(FlaskForm):
    arquivo_lote_arquivo = FileField('Arquivo:', [validators.DataRequired()], render_kw={"placeholder": "selecionar arquivo"})

##################################################################################################################################
#VENDA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: venda
#TIPO: edição
#TABELA: tb_venda
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_venda(FlaskForm):
    cod_lote = SelectField('Lote:', coerce=int, choices=[(g.cod_lote, g.matricula_lote) for g in tb_lote.query.all()])
    cod_cliente = SelectField('Cliente:', coerce=int, choices=[(g.cod_cliente, g.nome_cliente) for g in tb_cliente.query.all()])
    qtdparcelas_venda = IntegerField('Qtd Parcelas:', [validators.DataRequired()], render_kw={"placeholder": "digite o total de parcelas"})
    valorparcela_venda = DecimalField('Valor Parcelas:', [validators.DataRequired()], render_kw={"placeholder": "digite o total de parcelas"})
    diavenc_venda = IntegerField('Dia Vencimento:', [validators.DataRequired()], render_kw={"placeholder": "digite o total de parcelas"})
    data_venda = DateField('Data Venda:', [validators.DataRequired()], render_kw={"placeholder": "digite a data da venda do lote"})
    status_venda = SelectField('Situação:', coerce=int, choices=[(0, 'A Venda'),(1, 'Vendido')])

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: venda
#TIPO: visualização
#TABELA: tb_venda
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_venda(FlaskForm):
    cod_lote = SelectField('Lote:', coerce=int, choices=[(g.cod_lote, g.matricula_lote) for g in tb_lote.query.all()], render_kw={'readonly': True})
    cod_cliente = SelectField('Cliente:', coerce=int, choices=[(g.cod_cliente, g.nome_cliente) for g in tb_cliente.query.order_by('nome_cliente')], render_kw={'readonly': True})
    qtdparcelas_venda = IntegerField('Qtd Parcelas:', [validators.DataRequired()], render_kw={'readonly': True})
    valorparcela_venda = DecimalField('Valor Parcelas:', [validators.DataRequired()], render_kw={'readonly': True})
    diavenc_venda = IntegerField('Dia Vencimento:', [validators.DataRequired()], render_kw={'readonly': True})
    data_venda = DateField('Data Venda:', [validators.DataRequired()], render_kw={'readonly': True})
    status_venda = SelectField('Situação:', coerce=int, choices=[(0, 'A Venda'),(1, 'Vendido')], render_kw={'readonly': True})


##################################################################################################################################
#VENDA / ARQUIVO
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: lote / arquivo
#TIPO: edição
#TABELA: tb_lote_arquivo
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_venda_arquivo(FlaskForm):
    arquivo_venda_arquivo = FileField('Arquivo:', [validators.DataRequired()], render_kw={"placeholder": "selecionar arquivo"})

##################################################################################################################################
#VENDA PARCELA
##################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: venda
#TIPO: edição
#TABELA: tb_venda_parcela
#---------------------------------------------------------------------------------------------------------------------------------
class frm_editar_venda_parcela(FlaskForm):
    valorparcela_vendaparcela = DecimalField('Qtd Parcelas:', [validators.DataRequired()], render_kw={"placeholder": "digite o valor de parcelas"})
    datavenc_vendaparcela = DateField('Data Venda:', [validators.DataRequired()], render_kw={"placeholder": "digite a data da vencimento do lote"})
    datapag_vendaparcela = DateField('Data Pagamento:', [validators.DataRequired()], render_kw={"placeholder": "digite a data da pagamento do lote"})
    status_vendaparcela = SelectField('Situação:', coerce=int, choices=[(0, 'Em Aberto'),(1, 'Pago')])

#---------------------------------------------------------------------------------------------------------------------------------
#FORMUÁRIO: venda
#TIPO: visualização
#TABELA: tb_venda
#---------------------------------------------------------------------------------------------------------------------------------
class frm_visualizar_venda_parcela(FlaskForm):
    valorparcela_vendaparcela = DecimalField('Qtd Parcelas:', [validators.DataRequired()], render_kw={'readonly': True})
    datavenc_vendaparcela = DateField('Data Venda:', [validators.DataRequired()], render_kw={'readonly': True})
    datapag_vendaparcela = DateField('Data Pagamento:', [validators.DataRequired()], render_kw={'readonly': True})
    status_vendaparcela = SelectField('Situação:', coerce=int, choices=[(0, 'Em Aberto'),(1, 'Pago')], render_kw={'readonly': True})