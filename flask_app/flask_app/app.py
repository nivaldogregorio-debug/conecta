from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Configuração da conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="celsogama",
    database="aula"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        status = request.form['status']

        senha_hash = generate_password_hash(senha)

        try:
            cursor.execute("INSERT INTO usuario (login, senha, status) VALUES (%s, %s, %s)", (login, senha_hash, status))
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Erro ao cadastrar: {err}"

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        cursor.execute("SELECT * FROM usuario WHERE login = %s", (login,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['senha'], senha):
            if usuario['status'] == 'ativo':
                session['usuario'] = usuario['login']
                return redirect(url_for('painel'))
            else:
                return "Usuário inativo."
        else:
            return "Login ou senha inválidos."

    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'usuario' in session:
        return render_template('painel.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


