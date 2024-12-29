from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import barcode
from barcode import generate

# Crear un objeto de código de barras
codigo = barcode.get('code128', '123456789', writer=barcode.writer.ImageWriter())

# Guardar el código de barras en un archivo PNG
archivo_imagen = codigo.save('codigo_barras')

# Crear un documento PDF
pdf = canvas.Canvas('tickets.pdf', pagesize=letter)

# Agregar el código de barras al PDF
pdf.drawInlineImage('codigo_barras.png', x=100, y=100)

# Guardar el PDF
pdf.save()
