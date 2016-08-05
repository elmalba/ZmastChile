from flask import render_template,session,jsonify

import smtplib
from email.MIMEText import MIMEText
from email.Encoders import encode_base64
from sys import path
path.append("/var/www/Flask/lib")
from SQLcrowd import SQLcrowd
from mailer import mailer
class Data(object):
	def __init__(self,):
		self.menus=[1,'Inicio'],[7,'Marca','Historia','Marca','Calidad de Zamst','Concepto','Mapa','Lexico'],[1,'Productos'],[4,'Expertice Zamst','Procesos','Inovacion','Lesiones','Heridas y solucion'],[3,'Atletas y Medicos','Atletas','Medicos'],[3,'Comprar','Como comprar','Carro de compra'],[1,'Nosotros']
		self.info={'fono':'+56 (9) 7516 7616'}
		self.info.update({'email':'ventas@zamst.cl','fb':'hola','tw':'hola2'})
		self.info.update({'company':'Zamst'})
		self.info.update({'dir1':'Vitacura, '})
		self.info.update({'dir2':'Santiago , Chile'})
		self.sql = SQLcrowd("zamstchile")
		self.carrito=[]
		self.carro=[]
		self.monto=0
		self.cantidad=0
		session['carro']=[]
		session['monto']=0
		self.text="hol"

	def menu(self):
		print "holi"
	def header(self):
		return render_template("header.html",menus=self.menus,info=self.info)
	def footer(self):
		return render_template("footer.html",menus=self.menus,info=self.info)+render_template("javascripts.html",carro=session['carro'],monto=session['monto'])

	def inicio_template(self):
		Noticias = self.sql.select("noticias", ["id", "nombre", "resumen", "hashtag", "fecha","foto"], [["order by","id desc"],["limit "," 3"]])

		return self.header()+render_template("index.html",name="Zamst",blogdata=Noticias,problemas=self.sql.select("categoria_problema",["nombre","id_productos"],[["where id_productos is not ","null"]]),deporte=self.sql.select("categoria_deporte",["nombre","id_productos"],[["where id_productos is not ","null"]]),menus=self.menus,productos=self.sql.select("productos", ["id", "nombre", "to_char(precio, '999  990D') "], [["order by","ventas desc"],["Limit","8"]]))+self.footer()+"""
  		<script src="/static/jquery.bxslider.min.js"></script>
<!-- bxSlider CSS file -->
<link href="/static/jquery.bxslider.css" rel="stylesheet" />

		<script>$(document).ready(function(){
$('.bxslider').bxSlider({
  auto: true,
  autoControls: true
});
});</script>"""
	def contacto_template(self):
		return self.header()+render_template("contact.html",info=self.info)+self.footer()

	def inova_template(self):
		return self.header()+render_template("inova.html",info=self.info)+self.footer()+render_template("inovascript.html")


	def producto_template(self,idp):
		idp=idp.split("-")
		producto = self.sql.select("productos", ["id", "nombre", "cuerpo", "talla", "subtitulo","precio","tecnologias","video1","video2","stock"], [["where id =","'%s'"%idp[0]]])
		idcond=producto[0][6].split(";;")
		idcondicion=""
		largo=len(idcond)
		tecno=False
		for i in range(largo):
			idcondicion=idcondicion+"id = %s"%idcond[i]
			if i+1!=largo:
				idcondicion=idcondicion+" or "
			else:
				tecno=True
		try:
			if tecno==True:
				tecnologias=self.sql.select("tecnologia",["nombre","detalle","foto"],[["where ",idcondicion]])
			else:
				tecnologias=""
		except:
			tecnologias=""
		data={'id':producto[0][0],'nombre':producto[0][1],'text':producto[0][2].split(";;"),'talla':producto[0][3].split(";;"),'subtitulo':producto[0][3]}
		return self.header()+render_template("products_details3.html",data=data,tecnologias=tecnologias,producto=producto,recomendados=self.sql.execute("SELECT id, nombre, precio from productos,(select id_productos from categorias_productos where id_categorias = (select id_categorias from categorias_productos where id_productos='%s') and id_productos!='%s' order by random() limit 2) as resultados where id = resultados.id_productos and precio is not null"%(idp[0],idp[0])))+self.footer()

	def productos_template(self):
		categorias=self.sql.select("categorias_productos",["id_productos","id_categorias"],[["order by ","id_categorias asc"]])
		idp=1
		catarr=[]
		catarrtemp=[]
		for cat in categorias:
			if cat[1] != idp :
				catarr.append(catarrtemp)
				catarrtemp=[]
				idp=cat[1]
			catarrtemp.append(cat[0])
		catarr.append(catarrtemp)
		problemas=self.sql.select("categoria_problema",["nombre","id_productos"],[["where id_productos is not ","null"]])
		productos=self.sql.select("productos", ["id", "nombre", "to_char(precio, '999  990D') "], [["where precio ","is not null"],["order by","nombre asc"]])
		idp=1
		catarr2=[]
		catarrtemp=[]
		for cat in problemas:
			catarrtemp.append(cat[1].split(";;"))
		catarr2=catarrtemp
		deportes=self.sql.select("categoria_deporte",["nombre","id_productos"],[["where id_productos is not ","null"]])

		catarr3=[]
		catarrtemp=[]
		for cat in deportes:
			catarrtemp.append(cat[1].split(";;"))
		catarr3=catarrtemp
		

		return self.header()+render_template("products.html",catarr3=catarr3,deporte=deportes,catarr=catarr,catarr2=catarr2,problemas=problemas,categorias=self.sql.select("categorias", ["id", "nombre", "cantidad"], [["order by ","nombre asc"]]),productos=productos,lenprodu=len(productos),paginas=len(productos) /9 + 1 - pow(0, len(productos) % 9))+self.footer()

	def blog(self,name,page):
		Noticias = self.sql.select("noticias", ["id", "nombre", "resumen", "hashtag", "fecha","foto"], [["order by","id desc"]])
		return self.header()+render_template("blog.html",name=name,blogdata=Noticias)+self.footer()
	def blog_detalle(self,name,page):
		Noticias = self.sql.select("noticias", ["id", "nombre", "cuerpo", "hashtag", "fecha","foto"], [["where id=","'%s'"%str(page)],["order by","id desc"],["limit","3"]],True)
		return self.header()+render_template("blog_details.html",name=name,blog=Noticias)+self.footer()
	def atleta(self):
		return self.header()+render_template("atleta.html")+self.footer()
	def marca(self):
		return self.header()+render_template("marca.html")+self.footer()
	def lesiones(self):
		return self.header()+render_template("lesiones.html")+self.footer()

	def espalda(self):
		return self.header()+render_template("espalda.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id = 35 or id = 36 or id=37"))+self.footer()
	def hielo(self):
		return self.header()+render_template("hielo.html")+self.footer()
	def pie(self):
		return self.header()+render_template("pie.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id = 10 or id = 11"))+self.footer()

	def RodillaLigamento(self):
		return self.header()+render_template("rodilla.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id = 30 or id = 31 or id=32"))+self.footer()
	def Rodillasaltador(self):
		return self.header()+render_template("rodilla2.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id = 18 or id = 19 or id=17"))+self.footer()
	def RodillaTFL(self):
		return self.header()+render_template("rodilla3.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id =22"))+self.footer()


	def Tobillo(self):
		return self.header()+render_template("tobillo.html",recomendados=self.sql.execute("SELECT id, nombre, precio from productos where id = 3 or id = 1 or id=2 or id=8"))+self.footer()

	def shopping(self):
		return self.header()+render_template("shopping_cart.html")+self.footer()
	def checkout(self):
		return self.header()+render_template("checkout.html")+self.footer()

	def calidad(self):
		return self.header()+render_template("calidad.html")+self.footer()
	def procesos(self):
		return self.header()+render_template("procesos.html")+self.footer()

	def concepto(self):
		return self.header()+render_template("concepto.html")+self.footer()
	def historia(self):
		return self.header()+render_template("historia.html")+self.footer()
	def lexico(self):
		return self.header()+render_template("lexico.html")+self.footer()
	def mapa(self):
		return self.header()+render_template("mapa.html")+self.footer()


	def agregar_template(self,id_producto,cantidad):
		for producto in self.carrito:
			if int(producto[0]) == int(id_producto):
				producto[3]=cantidad+producto[3]
				self.monto=self.monto+(int(producto[4])*cantidad)
				self.cantidad=self.cantidad+cantidad
				return self.json()

		producto = self.sql.select("productos", ["id", "nombre","precio", "to_char(precio, '999G990D')"], [["where id =","'%s'"%id_producto]],True)
		self.monto=self.monto+(int(producto[2])*cantidad)
		self.cantidad=self.cantidad+cantidad
		self.carrito.append([producto[0],producto[1],producto[3].replace(",","."),cantidad,producto[2]])
		return self.json()
	def json(self,idp,cantidad):

			productos=self.sql.select("productos", ["id","nombre", "precio"], [["where id = ","'%s'"%idp]],True)
			info={'id':productos[0],'nombre': productos[1],'precio':productos[2],'cantidad':cantidad}
			temp=True
			for item in session['carro']:
				if int(item['id'])==int(idp):
					item['cantidad']=int(item['cantidad'])+int(cantidad)
					print item
					temp=False
			if temp:
				session['carro'].append(info)
			session['monto']=session['monto']+info['precio']*info['cantidad']
			print session['carro']
			print session['monto']
			
			return jsonify(data=info)
	def eliminar(self,idpos):
		arr=[]
		arrtemp=session['carro']
		largo = len(arrtemp)
		for i in range(largo):
			
			if int(i)!=int(idpos):
				print i 
				arr.append(arrtemp[i])
			else:
				session['monto']=session['monto']-(arrtemp[i]['cantidad']*arrtemp[i]['precio'])
		session['carro']=arr
		return ""
	def eliminar2(self,idpos,cantidad):
		arr=session['carro']
		monto=session['monto']-(int(arr[idpos]['cantidad'])*int(arr[idpos]['precio']))
		arr[idpos]['cantidad']=int(cantidad)
		monto=monto+(int(arr[idpos]['cantidad'])*int(arr[idpos]['precio']))
		session['carro']=arr
		session['monto']=monto
		print session['monto']
		return ""
	def order(self,data):
		print data[0].form
		variables=["nombre","apellido","rut","email","celular","redfija"]
		valores=[]
		for var in variables:
			valores.append(str(data[0].form[var]).lower())
		variables.append("direccion")
		valores.append(str(data[0].form["dir"]).lower()+str(data[0].form["comuna"]).lower()+str(data[0].form["city"]).lower()+str(data[0].form["region"]).lower())

		iduser=self.sql.insert("usuarios",variables,valores,True)
		idventa=self.sql.insert("ventas",["iduser","monto","estado","moneda"],[str(iduser),str(session['monto']),"0","CLP"],True)
		for carro in session['carro']:
			self.sql.insert("ventas_detalle",["idventa","producto","cantidad","monto"],[str(idventa),carro['nombre'],str(carro['cantidad']),str(carro['precio'])])
		
		
		mail=mailer("no-responder@crowdlatam.com","crowdlatamenvio","smtp.gmail.com",587)
		data_mail=render_template("email.html",carro=session['carro'],monto=session['monto'],idorder=idventa,info=data[0].form)
		mail.enviar(data[0].form['email'],"Ventas ZamstChile Orden N:%s"%idventa,data_mail)
		mail.enviar("nicolas@zamstchile.com","Ventas ZamstChile Orden N:%s"%idventa,data_mail)
		return jsonify(order=idventa)


	def json_mode(self,modo,pagina):
			productos=self.sql.select("productos", ["id", "nombre", "to_char(precio, '999  990D') "], [["order by","ventas desc"],["Limit","9"],["offset","%s"%(str(9*(int(pagina)-1)))]])
			Info="Info="
			for i in range(len(productos)):
				Info=Info+"{'id':productos["+str(i)+"][0],'nombre':productos["+str(i)+"][1],'precio':productos["+str(i)+"][2]},"
			
			exec(Info)
			list=[Info]
			return jsonify(productos=list)


	def semicarro_template(self):

		return render_template("javascripts.html")+render_template("semicarro.html",carrito=self.carrito,largo=self.cantidad,monto=('{:,}'.format(self.monto)).replace(",","."))



	def quitar_template(self,id_pos):
		id_pos=int(id_pos)
		self.monto=self.monto-self.carrito[id_pos][3]*self.carrito[id_pos][4]
		self.cantidad=self.cantidad-self.carrito[id_pos][3]
		self.carrito.pop(id_pos)
		return self.json()

	def error404(self):
		return self.header()+render_template('404.html')+self.footer()
"""
class email(object):

	def __init__(self):

		self.usuario = "web@tuasistencia.cl"
		self.contra = "correommae2010."
	

	def send(self,nombre,destino,asunto,cuerpo):

		print "hola"
		mensaje = MIMEText("Nombre:  "+nombre +" \nEmail : "+destino+"\n\n"+cuerpo)
		mensaje['From']=self.usuario
		mensaje['To']=self.usuario
		mensaje['Subject']=(asunto)
		mailServer = smtplib.SMTP("localhost")
		'''
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(self.usuario,self.contra)
		print "hola"
		'''
		mailServer.sendmail(self.usuario,
		                self.usuario,
		                mensaje.as_string())
		mailServer.close()

		return "work motherfucker"
"""

