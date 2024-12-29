from flask import *
import pymysql
from db import CBD
from sesion import userSession
import re
import base64
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import io

from db import CBD




cbd = CBD()
cbd.conectar()
ses = userSession()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

def comprimirImagen(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail((1000, 1000))  
    imgComprimida = io.BytesIO()
    img.save(imgComprimida, format='JPEG', quality=90)  
    return imgComprimida.getvalue()


@app.route('/')
def inicio():
    return render_template('iniciar.html')

@app.route('/index')
def index():
    return render_template('iniciar.html')


@app.route('/guardarImg', methods=['POST'])
def saveImg():
    if request.method == 'POST':
        prdctName = request.form['nombre']
        descrip = request.form['descrip']
        categoria = request.form['categoria']
        properts = request.form['propied']
        imagen = request.files['imagen']
        tipo = imagen.mimetype
        img_comprimida = comprimirImagen(imagen)
        costo = int(request.form['costo'])
        stock = int(request.form['stock'])
        
        cbd.cursor.execute('INSERT INTO productos (nombre, descripcion, categoria, propiedades, imagen, tipo, costo, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (prdctName, descrip, categoria, properts, img_comprimida, tipo, costo, stock))
        cbd.conection.commit()
    return redirect(url_for('mostrarImages'))


@app.route('/mostrarImgs')
def mostrarImages():
    cbd.cursor.execute('SELECT id, nombre, descripcion, imagen, tipo, costo, stock FROM productos')
    productos_raw = cbd.cursor.fetchall()

    productos = []
    for producto in productos_raw:
        idd, nombre, descripcion, imagen, tipo, costo, stock = producto
        imagen_base64 = base64.b64encode(imagen).decode("utf-8")
        productos.append((idd, nombre, descripcion, imagen_base64, tipo, costo, stock))

    return render_template('tablaImgs.html', products = productos)


@app.route('/addToCar', methods=['GET', 'POST'])
def addPrdctToCar():
    idUser = ses.idUsuario
    if request.method == 'POST':
        idPrdct = request.args.get('id_prdct')
        selecPrdcts = int(request.form['cantidad'])
        costo = request.args.get('precio')
    
    else:
        idPrdct = request.args.get('id_prdct')
        selecPrdcts = request.args.get('cantidad')
        costo = request.args.get('precio')
    
    try:
        cbd.cursor.execute("SELECT b.id_user, b.id_prdct, b.quant_prdcts, a.stock FROM carrito b JOIN productos a ON b.id_prdct=a.id WHERE b.id_user=%s and b.id_prdct=%s", (idUser, idPrdct))
        resul = cbd.cursor.fetchall()

        if len(resul) > 0:
            idd, idprd, cantPrds, stock = resul[0]

            if (selecPrdcts+cantPrds) > stock:
                mensaje = "Has seleccionado el límite de productos a agregar"
            
            else:
                cbd.cursor.execute("UPDATE carrito SET quant_prdcts=quant_prdcts + %s WHERE id_user=%s and id_prdct=%s", (selecPrdcts, idUser, idPrdct))
                cbd.conection.commit()

        else:
            cbd.cursor.execute("INSERT INTO carrito (id_user, id_prdct, quant_prdcts, precio_prdct) VALUES (%s, %s, %s, %s)", (idUser, idPrdct, selecPrdcts, costo))
            cbd.conection.commit()

        return redirect(url_for('verProducto', idPrdct = idPrdct))

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/updatePrdctInCar', methods=['GET', 'POST'])
def modificarPrdctInCar():
    idUser = ses.idUsuario
    if request.method == 'POST':
        idPrdct = request.args.get('id_prdct')
        #costo = request.args.get('precio')
        quantPrdcts = int(request.form['cantidad'])

    try:
        cbd.cursor.execute("UPDATE carrito SET quant_prdcts = %s WHERE id_user=%s AND id_prdct=%s", (quantPrdcts, idUser, idPrdct))
        cbd.conection.commit()

        return redirect(url_for('seePrdctSelect', idPrdctCar = idPrdct))

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/verPrdct/<string:idPrdct>')
def verProducto(idPrdct):
    idUser = ses.idUsuario
    try:
        cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.categoria, a.propiedades, a.imagen, a.tipo, a.costo, a.stock, (SELECT quant_prdcts FROM carrito WHERE id_user=%s AND id_prdct=%s) AS productosCar FROM productos a WHERE a.id=%s", (idUser, idPrdct, idPrdct))
        producto_list = cbd.cursor.fetchall()

        producto = []
        for prdct in producto_list:
            idd, nombre, descrip, catego, propie, image, tipo, costo, stock, prdctsInCar = prdct
            imagen_base64 = base64.b64encode(image).decode("utf-8")
            producto.append((idd, nombre, descrip, catego, propie, imagen_base64, tipo, costo, stock, prdctsInCar))
       
        return render_template('producto.html', producto = producto)
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/verProductoSelec/<string:idPrdctCar>')
def seePrdctSelect(idPrdctCar):
    idUser = ses.idUsuario
    try:
        cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.categoria, a.propiedades, a.imagen, a.tipo, a.costo, a.stock, b.quant_prdcts FROM productos a JOIN carrito b ON a.id=b.id_prdct WHERE b.id_user=%s AND a.id=%s", (idUser, idPrdctCar))
        data = cbd.cursor.fetchall()

        infoProduct = []
        for ide in data:
            idd, nombre, descripcion, catego, propert, image, tipo, costo, stock, producsSelec = ide
            total = int(producsSelec) * int(costo)
            imagen_base64 = base64.b64encode(image).decode("utf-8")
            infoProduct.append((idd, nombre, descripcion, catego, propert, imagen_base64, tipo, costo, stock, producsSelec, total))

        return render_template('productoEnCar.html', productoCar = infoProduct)

    except pymysql.Error as err:
        return render_template('error.html', error = err)

class Carrito():
    @app.route('/carrito')
    def carrito():
        idUser = ses.idUsuario
        try:
            cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.imagen, a.tipo, a.costo FROM productos a JOIN carrito b ON a.id=b.id_prdct WHERE b.id_user=%s ORDER BY a.id", (idUser))
            data = cbd.cursor.fetchall()

            infoProducts = []
            total = 0
            for ide in data:
                idd, nombre, descripcion, image, tipo, costo, producsSelec = ide
                imagen_base64 = base64.b64encode(image).decode("utf-8")
                infoProducts.append((idd, nombre, descripcion, imagen_base64, tipo, costo, producsSelec))
                total += int(costo) * int(producsSelec)

            return render_template('carrito.html', productosCar = infoProducts, total = total)

        except pymysql.Error as err:
            return render_template('error.html', error = err)


@app.route('/eliminarPrdctCar/<string:idPrdct>')
def deletePrdctCar(idPrdct):
    idUser = ses.idUsuario
    idPrdctCar = idPrdct

    try:
        cbd.cursor.execute("DELETE FROM carrito WHERE id_user=%s and id_prdct=%s", (idUser, idPrdctCar))
        cbd.conection.commit()

        return redirect(url_for('carrito'))
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/ticket')
def ticket():

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
    pdf.cell(0, 10, f'#{idd}   {nombre}        ${costo}', 0, 1, 'C')
    pdf.cell(0, 10, f'Descripción: {descripcion}', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, 'TOTAL: {total}', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, 'ESTE NO ES UN COMPROBANTE FISCAL', 0, 1, 'C')


    pdf.output('ticket_compra.pdf')
    

if __name__ == "__main__" :
    app.run(debug=True)
