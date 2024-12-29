from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required,UserMixin

import pymysql
import re

from config import config
from database.db import CBD

cbd = CBD()
cbd.conectar()
app = Flask(__name__)

csrf = CSRFProtect()
login_manager_app = LoginManager(app)




@app.route('/')
def home():
    return render_template('home.html')


# R E G I S T R O
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods=["POST"])
def crear_registro(): 
    if request.method == "POST":
        nombrec = request.form['nombrec'] 
        correo = request.form['correo']
        numcel = request.form['numcel']
        direc = request.form['direc']
        contraseña = request.form['contraseña']
        contraseña1 = request.form['contraseña1']

        try:
            cbd.cursor.execute("SELECT correo FROM usuarios WHERE correo = %s", (correo,))
            us_existente = cbd.cursor.fetchone()

            if us_existente:
                return "Con este correo ya existe una cuenta"

            if contraseña == contraseña1:

                contraseña_encriptada = generate_password_hash(contraseña1, 'sha256', 30)
                
                cbd.cursor.execute("INSERT INTO usuarios (nombrec, correo, numcel, direc, contraseña_encriptada, id) VALUES (%s, %s, %s, %s, %s, '4')",(nombrec,correo,numcel,direc,contraseña_encriptada))
                cbd.conection.commit()
                
                return render_template("register.html",mensaje="Usuario Registrado Exitosamente")
            else:
                return "Las contraseñas no coinciden"
            
        except Exception as e:
            cbd.conection.rollback()
            return f"Error: {str(e)}"
        finally:
            cbd.cursor.close()
            cbd.conection.close()    

    else:
        return "Método no permitido"


# T E R M I N O

# I N I C I O  D E  S E S I Ó N

class User(UserMixin):
    def __init__(self, id, correo, contraseña):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña

@login_manager_app.user_loader
def load_user(id):
    sql = "SELECT id, correo, contraseña FROM usuarios WHERE id = %s"
    with cbd.conection.cursor() as cursor:
        cursor.execute(sql, (id,))
        user_data = cursor.fetchone()
        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
            return user
        else:
            return None

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'correo' in request.form and 'contraseña' in request.form:
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        cur = cbd.conection.cursor()
        cur.execute('SELECT id, correo, contraseña_encriptada FROM usuarios WHERE correo = %s', (correo,))
        nombrec = cur.fetchone()

        if correo and check_password_hash(correo['contraseña_encriptada'], contraseña):
            session['logueado'] = True
            session['id'] = correo['id']
            return render_template("home.html")
        
        elif nombrec and check_password_hash(nombrec['contraseña_encriptada'], 'B!1w8NAt1T^%kvhUI*S^'):
            return render_template("admin.html")

        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrectas")

    return render_template('index.html', mensaje="Por favor, inicie sesión.")

# T E R M I N O

# C E R R A R  S E S I Ó N

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# T E R M I N O

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()