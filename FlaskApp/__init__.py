import os
from flask import request, session, g, redirect
from flask import url_for
from flask import Flask
from flask import render_template
import template

app = Flask(__name__)
DEBUG = True
app = Flask(__name__)
app.secret_key = 'Linateamo'



@app.route('/')
@app.route('/index')
@app.route('/inicio')
@app.route('/Inicio')
def index():
    Data=sessionserver()
    return Data.inicio_template()

@app.route('/inicio2')
def inicio2():
    header=render_template("header.html")
    center=render_template("inicio2_template.html")
    footer=render_template("footer.html")
    Data=sessionserver()
    return header+center+footer


@app.route('/Nosotros')
def Contacto():
    Data=sessionserver()
    return Data.contacto_template()

@app.route('/Producto/<url>')
def Producto(url=None):
    Data=sessionserver()
    return Data.producto_template(url)


@app.route('/Inovacion')
def inova():
    Data=sessionserver()
    return Data.inova_template()

@app.route('/Productos/')
def Productos(categoria=""):
    Data=sessionserver()
    return Data.productos_template()
@app.route('/Atletas')
def Atleta():
    Data=sessionserver()
    return Data.atleta()
@app.route('/Lesiones')
def lesiones():
    Data=sessionserver()
    return Data.lesiones()
@app.route('/Lesiones/Espalda')
def Espalda():
    Data=sessionserver()
    return Data.espalda()

@app.route('/Lesiones/Hielo')
def Hielo():
    Data=sessionserver()
    return Data.hielo()
@app.route('/Lesiones/Pie')
def Pie():
    Data=sessionserver()
    return Data.pie()
@app.route('/Lesiones/Rodilla-Ligamento')
def RodillaLigamento():
    Data=sessionserver()
    return Data.RodillaLigamento()

@app.route('/Lesiones/Rodilla-saltador')
def Rodillasaltador():
    Data=sessionserver()
    return Data.Rodillasaltador()
@app.route('/Lesiones/Rodilla-TFL')
def RodillaTFL():
    Data=sessionserver()
    return Data.RodillaTFL()

@app.route('/Lesiones/Tobillo')
def Tobillo():
    Data=sessionserver()
    return Data.Tobillo()


@app.route('/Productos/categoria/<categoria>')
def Productos_categoria(categoria):
    Data=sessionserver()
    return Data.productoscategoria_template(categoria)

@app.route('/Agregar/<id_producto>/<cantidad>')
def Agregar(id_producto,cantidad):
    Data=sessionserver()
    return Data.agregar_template(str(int(id_producto)),int(cantidad))
@app.route('/Medicos')
@app.route('/Medicos/<page>')
def blog(page="0"):
    Data=sessionserver()
    return Data.blog("Medicos",int(page))
@app.route('/Medicos/detalle/<page>')
def blog_detalle(page="0"):
    print int(str(page).split("-")[0])
    Data=sessionserver()
    return Data.blog_detalle("Medicos",int(str(page).split("-")[0]))
@app.route('/Marca')
def marca():
    Data=sessionserver()
    return Data.marca()
@app.route('/Calidad de Zamst')
def calidad():
    Data=sessionserver()
    return Data.calidad()
@app.route('/Concepto')
def concepto():
    Data=sessionserver()
    return Data.concepto()
@app.route('/Historia')
def historia():
    Data=sessionserver()
    return Data.historia()
@app.route('/Lexico')
def lexico():
    Data=sessionserver()
    return Data.lexico()
@app.route('/Mapa')
def mapa():
    Data=sessionserver()
    return Data.mapa()

@app.route('/Procesos')
def procesos():
    Data=sessionserver()
    return Data.procesos()

@app.route('/Semicarro')
def Semicarro():
    Data=sessionserver()
    return Data.semicarro_template()
@app.route('/data/<idp>')
@app.route('/data/<idp>/<cantidad>')
def Json(idp,cantidad=1):
    Data=sessionserver()
    return Data.json(int(idp),int(cantidad))
@app.route('/eliminar/<idp>')
def delete(idp):
    Data=sessionserver()
    return Data.eliminar(int(idp))

@app.route('/Ncantidad/<idp>/<cantidad>')
def Ncantidad(idp,cantidad=1):
    Data=sessionserver()
    return Data.eliminar2(int(idp),int(cantidad))



@app.route('/shopping')
@app.route('/cart')
@app.route('/Carro de compra')
def shop():
    Data=sessionserver()
    return Data.shopping()
@app.route('/checkout')
@app.route('/Como comprar')
def checkout():
    Data=sessionserver()
    return Data.checkout()

@app.route('/json/<modo>/<pag>')
def JsonM(modo,pag):
    Data=sessionserver()
    return Data.json_mode(modo,pag)

def sessionserver():
       return template.Data()

@app.route('/hola')
def hola():
    Data=sessionserver()
    session['value']=Data
    return str(Data.monto)
@app.route('/order', methods=['GET', 'POST'])
def order():
    Data=sessionserver()
    return Data.order([request])


@app.route('/Quitar/<id_pos>')
def Quitar(id_pos):
    Data=sessionserver()
    return Data.quitar_template(int(id_pos))

@app.route('/send', methods = ['POST'])
def send():
    mail=template.email()
    return mail.send(str(request.form['fullName']),str(request.form['email']),str(request.form['subject']),str(request.form['message']))
    
@app.errorhandler(404)
def page_not_found(e):
    Data=sessionserver()
    return Data.error404(), 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
