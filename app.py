from flask import Flask, render_template, request, redirect, make_response, session, url_for
from flask_sqlalchemy import SQLAlchemy
from scanner import scan_host
from werkzeug.security import generate_password_hash, check_password_hash
import pdfkit
import json
import os

# tenta configurar wkhtmltopdf em Windows
wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

if not os.path.isfile(wkhtmltopdf_path):
    # fallback para Progra~1
    wkhtmltopdf_path = r"C:\Progra~1\wkhtmltopdf\bin\wkhtmltopdf.exe"

if not os.path.isfile(wkhtmltopdf_path):
    raise FileNotFoundError("wkhtmltopdf não encontrado. Verifique a instalação.")

config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

app = Flask(__name__)
#Config DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "123456qwerty"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():

    if "username" not in session:
        return redirect(url_for("login"))
    
    scan_results = None
    error = None

    if request.method == 'POST':
        target = request.form.get('target')
        if target:
            scan_results = scan_host(target)
            if "error" in scan_results[0]:
                error = scan_results[0]["error"]
                scan_results = None
        else:
            error = "Por favor, insira um IP ou domínio"
    
    return render_template('index.html', results=scan_results, error=error)


@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    host = request.form.get('host')
    results_json = request.form.get('results')
    results = json.loads(results_json)

    html = f"""
    <h1>Relatorio de Scanner - {host}</h1>
    """

    for h in results:
        html += f"<h2>Host: {h['host']} ({h['hostname']}) - Estado: {h['state']}</h2>"
        for proto in h['protocols']:
            html += f"<h3>Protocolo: {proto['protocol']}</h3>"
            html += """
            <table border="1" cellspacing="0" cellpadding="4">
                <tr>
                    <th>Porta</th>
                    <th>Estado</th>
                    <th>Serviço</th>
                </tr>
            """
            for port in proto['ports']:
                html += f"<tr><td>{port['port']}</td><td>{port['state']}</td><td>{port['service']}</td></tr>"
            html += "</table><br>"

    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
    except Exception as e:
        return f"Erro ao gerar PDF: {e}", 500

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Relatorio.pdf'
    return response

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        #Valida os dados
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return render_template("register.html", message="All fields are required")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", message = "Utilizador já existe")
        #Hash da password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()

        #check se o username e a password estão corretos
        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect ("/")
        else:
            return render_template("login.html", message="Invalid Username or password")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == '__main__':
    app.run(debug=True)
