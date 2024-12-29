from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)

@app.route('/')
def home():

    return render_template("home.html")


@app.route('/areaT', methods=['GET', 'POST'])
def areaT():
    
    area = 0

    if request.method == 'POST':
        
        a = int(request.form['base'])
        b = int(request.form['altura'])
        area = b * a / 2

    return render_template("areat.html", res = area)


@app.route('/grados', methods=['GET', 'POST'])
def grados():

    centi = 0

    if request.method == 'POST':
        f = int(request.form['fharen'])
        centi = (f - 32) * (5/9)

    return render_template("grados.html", r = centi)


@app.route('/calf', methods=['GET', 'POST'])
def calfs():
    r = ""
    if request.method == 'POST':
        num = int(request.form['num'])
        
        if num <= 5:
            r= 'REPROBADO'
        elif num == 6:
            r= 'SUFICIENTE'
        elif num == 7:
            r= 'REGULAR'
        elif num >= 8 and num <= 9:
            r= 'NOTABLE'
        elif num == 10:
            r= 'EXCELENTE'

    return render_template("calf.html", resu = r)


@app.route('/viaje', methods=['GET', 'POST'])
def viaje():
    p = ""

    if request.method == 'POST':
        nalu = int(request.form['num'])

        if nalu >= 50 and nalu <= 99:
            p = '$70'
        elif nalu >= 30 and nalu <= 49:
            p = '$95'
        elif nalu < 30:
            p = '$3500'

    return render_template("viaje.html", r = p)


@app.route('/tablamult', methods=['GET', 'POST'])
def tablamult():

    n = 0

    if request.method == 'POST':
        num = int(request.form['num'])

        if num >= 2 and num <= 10:
            t = [(i, num * i) for i in range(1, 11)] 
            return render_template('tablamult.html', numero=num, tabla=t)
        
        else:
            return "El número debe estar entre 2 y 10."
        
    else:
        return render_template('tablamult.html')

if __name__ == "__main__":
    app.run(debug=True)
