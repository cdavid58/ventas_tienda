from django.db import models
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.conf import settings
from datetime import date
from datetime import datetime


class Categoria(models.Model):
	nombre = models.CharField(max_length = 50)
	img = models.ImageField(upload_to="categoria",null=True)


class Producto(models.Model):
	articulo = models.CharField(max_length=250)
	img = models.ImageField(upload_to="producto",null=True)
	precio = models.CharField(max_length=10)
	categoria = models.ForeignKey(Categoria,on_delete= models.CASCADE)


class Usuario(models.Model):
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	telefono = models.CharField(max_length=10)
	email = models.EmailField()
	direccion = models.TextField()


class Factura(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete = models.CASCADE)
	articulo = models.CharField(max_length=250)
	precio = models.CharField(max_length=10)
	fecha = models.CharField(max_length=10,default=date.today())
	cantidad = models.CharField(max_length=20,default=0)
	formaPago = models.CharField(max_length=50,default="")


class referencia(models.Model):
	refe = models.CharField(max_length=1000)


class Carrito(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def add(self,producto,cantidad = 0,cat = None):
		#del self.cart[str(producto.pk)]
		#print(self.cart[str(producto.pk)],'ID CARRO')

		#cantidades = self.cart[str(producto.pk)]

		total = float(producto.precio) * float(cantidad)
		if str(producto.pk) in self.cart:
			pass
		else:
			self.request.session['carrito'] +=1
		print('Entre al else que pasa')
		self.cart[str(producto.pk)] = {'codigo':producto.pk,'articulo':producto.articulo,'cantidad':cantidad,'precio':producto.precio,'total':total,'img':producto.img.url,'cat':cat}
		'''if int(cantidad) < int(cantidades['cantidad']):

			if str(producto.pk) in self.cart:
					print('Entre al if')
					#del self.cart[str(producto.pk)]
					cnt = self.cart[str(producto.pk)]
					s = int(cnt['cantidad']) - int(cantidad)
					print(s,'cantidad')
					t = float(producto.precio) * float(s)
					cnt['total'] = t
					cnt['cantidad'] = s
					self.save()
		else:
			if str(producto.pk) in self.cart:
					print('Entre al if')
					#del self.cart[str(producto.pk)]
					cnt = self.cart[str(producto.pk)]
					s = int(cnt['cantidad']) + int(cantidad)
					print(s,'cantidad')
					t = float(producto.precio) * float(s)
					cnt['total'] = t
					cnt['cantidad'] = s
					self.save()
			else:'''
				# total = float(producto.precio) * float(cantidad)
				# self.request.session['carrito'] += 1
				# print('Entre al else que pasa')
				# self.cart[str(producto.pk)] = {'codigo':producto.pk,'articulo':producto.articulo,'cantidad':cantidad,'precio':producto.precio,'total':total,'img':producto.img.url,'cat':cat}
			
		print(self.cart)

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Producto.objects.filter(id__in=product_ids)
		'''for product in products:
			self.cart[str(product.id)]['product']=product'''

		for item in self.cart.values():
			#item['precio']=Decimal(item['precio'])
			#item['total']=item['precio']*item['cantidad']
			yield item


	def __len__(self):
		return sum(item['cantidad'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
