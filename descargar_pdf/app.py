from flask import *
from fpdf import FPDF
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_file
import pymysql

from database.db import CBD
from config import config

cbd = CBD()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        if 'ticket' in request.form:
            return redirect(url_for('generar_ticket'))
        le
        
    return render_template("home.html")
        

@app.route('/generar_ticket', methods=['GET', 'POST'])
def generar_ticket():
    if request.method == 'POST':
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 35)
                self.cell(0, 10, 'T C A O S - E', 0, 1, 'C')
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Ticket de compra', 0, 1, 'C')

                self.cell(0, 10, '==============================================', 0, 1, 'C')
                self.cell(0, 10, f'Fecha y hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
                self.cell(0, 10, '==============================================', 0, 1, 'C')

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        pdf.cell(0, 10, '==============================================', 0, 1, 'C')
        pdf.cell(0, 10, f'#1   JUAN        $700', 0, 1, 'C')
        pdf.cell(0, 10, f'Descripción: NEGRO BUENO PARA NADA', 0, 1, 'C')
        pdf.cell(0, 10, '==============================================', 0, 1, 'C')
        pdf.cell(0, 10, '==============================================', 0, 1, 'C')
        pdf.cell(0, 10, 'TOTAL: $780', 0, 1, 'C')
        pdf.cell(0, 10, '==============================================', 0, 1, 'C')
        pdf.cell(0, 10, 'ESTE NO ES UN COMPROBANTE FISCAL', 0, 1, 'C')

        pdf_file = 'ticket_compra.pdf'
        pdf.output(pdf_file)

        return send_file(pdf_file, as_attachment=True)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)