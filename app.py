from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('donenergy.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        email TEXT,
        sistema TEXT,
        valor REAL
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('donenergy.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projetos')
    projetos = c.fetchall()
    conn.close()
    return render_template('dashboard.html', projetos=projetos)
# Comentário para forçar novo deploy

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        cliente = request.form['cliente']
        email = request.form['email']
        sistema = request.form['sistema']
        valor = request.form['valor']
        conn = sqlite3.connect('donenergy.db')
        c = conn.cursor()
        c.execute("INSERT INTO projetos (cliente, email, sistema, valor) VALUES (?, ?, ?, ?)",
                  (cliente, email, sistema, valor))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('cadastro.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)