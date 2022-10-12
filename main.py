from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime 

# Iniciar banco de dados
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite'

app.secret_key = '13579'


db = SQLAlchemy(app) 
class Usuario(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    p_nome = db.Column(db.String(150))
    s_nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    data_de_nasciment0 = db.Column(db.String)
    senha = db.Column(db.Integer)
    senha_confirme = db.Column(db.Integer)
    
    def __init__(self, p_nome, s_nome, email, dt_nascimento, senha, senha_confirme):
        self.p_nome = p_nome
        self.s_nome = s_nome
        self.email = email
        self.dt_nascimento = dt_nascimento
        senha = senha
        senha_confirme = senha_confirme
                    

# Puxar rota onde ficam os usuários
@app.route('/')
def login():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios = usuarios)
    

# Cadastrar um novo usuário    
@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    if request.method == 'POST':
        usuario = Usuario(request.form['p_nome'], request.form['s_nome'], request.form['email'], request.form['dt_nascimento'], request.form['senha'], request.form['senha_confirme'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastro.html')


# Deletar um usuário (pelo id)
@app.route('/delete/<int:id>')
def delete(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('login'))


# Editar ou atualizar um usuário (pelo id)
@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.p_nome = request.form['p_nome']
        usuario.s_nome = request.form['s_nome']
        usuario.email = request.form['email']
        usuario.dt_nascimento = request.form['dt_nascimento']
        usuario.senha = request.form['senha']
        usuario.senha_confirme = request.form['senha_confirme']
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('edit.html', usuario = usuario)


# Login ( AINDA EM DESENVOLVIMENTO )
@app.route('/login', methods = ['GET', 'POST'])
def acesso():
    if request.method == 'POST' and request.form['nome'] != '':
        session['nome'] = request.form['nome']
        return redirect(url_for('index'))
        db.session.commit()
    return render_template('login.html')



# Logout ( AINDA EM DESENVOLVIMENTO )
@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    

# ! Faltando fazer autenticação de usuários !
# ! Armazenar dados da data do usuário(dia, mês e ano) !
# ! Conectar ao banco de dados !
    