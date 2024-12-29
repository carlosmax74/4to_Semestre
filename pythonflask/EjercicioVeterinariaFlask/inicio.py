from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")


@app.route('/nutria')
def nutri():
    return render_template("nutria.html")

@app.route('/nuestrosservicios')
def nuestrosservicios():
    return render_template("nuestrosservicios.html")

@app.route('/minipig')
def minipig():
    return render_template("minipig.html")

@app.route('/descp')
def descp():
    return render_template("descp.html")

@app.route('/conejo')
def conejo():
    return render_template("conejo.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/modificar')
def modificar():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria')
    cursor = conn.cursor()
    cursor.execute('select id, correo, comentarios from registro order by id')
    datos = cursor.fetchall()
    
    return render_template("modificar.html", comentarios = datos)


@app.route('/registro', methods=['POST'])
def añadir():
    if request.method == 'POST':
        aux_Correo = request.form['correo']
        aux_Comentarios = request.form['comentarios']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria' )
        cursor = conn.cursor()
        cursor.execute('insert into registro (correo,comentarios) values (%s, %s)',(aux_Correo, aux_Comentarios))
        conn.commit()
    return redirect(url_for('home'))


@app.route('/editar/<string:id>')
def editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria')
    cursor = conn.cursor()
    cursor.execute('select id, correo, comentarios from registro where id = %s', (id))
    dato  = cursor.fetchall()
    
    return render_template("editar.html", comentar=dato[0])

@app.route('/editar_comenta/<string:id>',methods=['POST'])
def editar_comenta(id):
    if request.method == 'POST':
        corr=request.form['correo']
        come=request.form['comentarios']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria')
        cursor = conn.cursor()
        cursor.execute('update registro set correo=%s, comentarios=%s where id=%s', (corr,come,id))
        conn.commit()
    return redirect(url_for('modificar'))

@app.route('/borrar/<string:id>')
def borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria')
    cursor = conn.cursor()
    cursor.execute('delete from registro where id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('modificar'))

@app.route('/insertar')
def insertar():
    return render_template("modificar.html")

@app.route('/agrega_comenta', methods=['POST'])
def agrega_comenta():
    if request.method == 'POST':
        aux_Correo = request.form['correo']
        aux_Comentarios = request.form['comentarios']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='veterinaria' )
        cursor = conn.cursor()
        cursor.execute('insert into registro (correo,comentarios) values (%s, %s)',(aux_Correo, aux_Comentarios))
        conn.commit()
    return redirect(url_for('modificar'))

if __name__ == "__main__":
    app.run(debug=True)

