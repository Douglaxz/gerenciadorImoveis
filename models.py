from gerenciadorImoveis import db

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_user(db.Model):
    cod_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    password_user = db.Column(db.String(50), nullable=False)
    status_user = db.Column(db.Integer, nullable=False)
    login_user = db.Column(db.String(50), nullable=False)
    cod_usertype = db.Column(db.Integer, nullable=False)
    email_user = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TIPO USUÁRIOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_usertype(db.Model):
    cod_usertype = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc_usertype = db.Column(db.String(50), nullable=False)
    status_usertype = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    
 
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: CLIENTES
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_clientes(db.Model):
    cod_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(50), nullable=False)
    nomefantasia_cliente = db.Column(db.String(50), nullable=False)
    end_cliente = db.Column(db.String(50), nullable=False)
    numend_cliente = db.Column(db.String(50), nullable=False)
    bairro_cliente = db.Column(db.String(50), nullable=False)
    cidade_cliente = db.Column(db.String(50), nullable=False)
    uf_cliente = db.Column(db.String(50), nullable=False)
    complemento_cliente = db.Column(db.String(50), nullable=False)
    cpf_cliente = db.Column(db.String(50), nullable=False)
    status_cliente = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    


#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TERRENO
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_terreno(db.Model):
    cod_terreno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    end_terreno = db.Column(db.String(50), nullable=False)
    nome_terreno = db.Column(db.String(50), nullable=False)
    end_cliente = db.Column(db.String(50), nullable=False)
    num_terreno = db.Column(db.String(50), nullable=False)
    bairro_terreno = db.Column(db.String(50), nullable=False)
    cidade_terreno = db.Column(db.String(50), nullable=False)
    uf_terrreno = db.Column(db.String(50), nullable=False)
    matricula_terreno = db.Column(db.Integer, nullable=False)
    status_terreno = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
    
#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TERRENO_ARQUIVOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_terreno_arquivos(db.Model):
    cod_terrenoarquivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_terreno = db.Column(db.Integer, nullable=False)
    arquivo_terrenoarquivo = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name    

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: LOTE          
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_lote(db.Model):
    cod_lote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_terreno = db.Column(db.Integer, nullable=False)
    status_lote = db.Column(db.String(50), nullable=False)
    valortotal_lote = db.Column(db.Float, nullable=False)
    matricula_lote = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: TERRENO_ARQUIVOS
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_lote_arquivos(db.Model):
    cod_lotearquivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_lote = db.Column(db.Integer, nullable=False)
    arquivo_lotearquivo = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name   

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: VENDA          
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_venda(db.Model):
    cod_venda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_lote = db.Column(db.Integer, nullable=False)
    cod_cliente = db.Column(db.Integer, nullable=False)
    status_venda = db.Column(db.String(50), nullable=False)
    qtdparcelas_venda = db.Column(db.Integer, nullable=False)
    valorparcela_venda = db.Column(db.Float, nullable=False)
    diavenc_venda = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#---------------------------------------------------------------------------------------------------------------------------------
#TABELA: VENDA_PARCELA
#ORIGEM: BANCO DE DADOS
#---------------------------------------------------------------------------------------------------------------------------------
class tb_venda_parcela(db.Model):
    cod_vendaparcela = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_venda = db.Column(db.Integer, nullable=False)
    cod_cliente = db.Column(db.Integer, nullable=False)
    status_vendaparcela = db.Column(db.String(50), nullable=False)
    valorparcela_vendaparcela = db.Column(db.Float, nullable=False)
    datavenc_vendaparcela = db.Column(db.Integer, nullable=False)
    datapag_vendaparcela = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
