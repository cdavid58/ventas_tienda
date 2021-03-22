from django.shortcuts import render, redirect
from django.http import HttpResponse
from .pago import *
from .models import *


def returnValueCart(request):
	return request.session['carrito']

def login(request):
	if 'carrito' in request.session:
		pass
	else:
		request.session['carrito'] = 0

	if request.method == 'POST':
		request.session['tlfUsario'] = request.POST.get('username')
		return redirect('categoria')
	return render(request,'login.html')


def categoria(request):
	c = Categoria.objects.all()
	return render(request,'categoria.html',{'c':c})


def listado(request,pk):
	c = Categoria.objects.all()
	request.session['cat'] = pk
	if request.is_ajax():
		cart_add(request,int(request.GET.get('dato')), request.GET.get('cant'), request.GET.get('cat'))
		return HttpResponse(returnValueCart(request))
		
	nombre = ""
	cat = Categoria.objects.filter(pk=pk)
	for i in cat:
		nombre = i.nombre
	p = Producto.objects.filter(categoria = Categoria.objects.get(pk=pk))

	return render(request,'listado.html',{'c':c,'cart':returnValueCart(request),
											'nombre':nombre,'cat':cat, 'p':p,'pk':request.session['cat']
										})



def viewCart(request):
	c = Categoria.objects.all()
	cart = Carrito(request)
	#tarjeta = Card(number = "4242424242424242",exp_month="06",exp_year="29",cvc="124",card_holder="Pedro Pérez")
	#print(tarjeta.tokenAceptacion(),'Estado')
	monto = 0
	for i in cart:
		monto += float(i['total'])

	ref = referencia.objects.get(pk=1)

	if request.method == 'POST':
		if request.POST.get('codigo') == '1':
			for i in cart:
				Factura(
					usuario = Usuario.objects.get(telefono=request.session['tlfUsario']),
					articulo = i['articulo'],
					precio = i['precio'],
					cantidad = i['cantidad'],
					formaPago = request.POST.get('formaPago')
				).save()
			a = int(ref.refe) + 1
			ref.refe = a
			ref.save()
		else:
			Usuario(
				nombre = request.POST.get('nombre'),
				apellido = request.POST.get('apellido'),
				telefono = request.session['tlfUsario'],
				email = request.POST.get('email'),
				direccion = request.POST.get('direccion')
			).save()
			for i in cart:
				Factura(
					usuario = Usuario.objects.get(telefono=request.session['tlfUsario']),
					articulo = i['articulo'],
					precio = i['precio'],
					cantidad = i['cantidad'],
					formaPago = request.POST.get('formaPago')
				).save()
			a = int(ref.refe) + 1
			ref.refe = a
			ref.save()
		return redirect('invoice')

	if request.is_ajax():
		cart_remove(request,request.GET.get('pk'))
		return HttpResponse(returnValueCart(request))
	try:
		cliente = Usuario.objects.get(telefono=request.session['tlfUsario'])
	except Usuario.DoesNotExist:
		cliente = None
	no_existe = 0
	if cliente is not None:
		no_existe = 1

	return render(request,'cart.html',{'c':c,'cart':returnValueCart(request),
											'cartShop':cart,'monto': str(monto).replace('.',''),'no_existe':no_existe,'refe':ref.refe
										})


def invoice(request):
	cart = Carrito(request)
	if len(cart) > 0:
		carting = cart
		subTotal = 0
		total = 0
		descuento = 0

		for i in carting:
			subTotal += float(i['total'])
			total += float(i['total'])

		usr = Usuario.objects.get(telefono=request.session['tlfUsario'])
		fact = Factura.objects.filter(usuario = usr).last()
		request.session['carrito'] = 0
		return render(request,'invoice.html',{'total':total, 'subTotal':subTotal,
												'cart':returnValueCart(request),
												'carShop':cart,'descuento':descuento,'usr':usr,
												'f':fact
											})
	else:
		return HttpResponse("Error 404")




def cart_add(request,product_id,cantidad,cat):
	producto = Producto.objects.get(pk=product_id,categoria=cat)
	cart = Carrito(request)
	#cantidad = request.GET.get('cantidad')
	cart.add(producto,int(cantidad))


def cart_remove(request,product_id):
	#product_id = request.GET.get('id')
	cart = Carrito(request)
	product = Producto.objects.get(pk=product_id)
	cart.remove(product)
	a = request.session['carrito']
	v = int(a) - 1
	request.session['carrito'] = v
	return redirect('/carrito/')




























