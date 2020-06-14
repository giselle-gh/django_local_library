from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario, Trayecto, Mensaje, Vehiculo, Pago
from .forms import RegistrationForm, LoginForm, TrayectoForm, ContactoForm, PasswordForm, PersonalForm, CocheForm, FotoForm, BuscarForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.utils import timezone
import re
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from appjobcar.models import *
from django.contrib.auth.hashers import make_password
#imports para paypal
from django.http import JsonResponse
import json
#import para mandar email
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import (
    DEFAULT_ATTACHMENT_MIME_TYPE, BadHeaderError, EmailMessage,
    EmailMultiAlternatives, SafeMIMEMultipart, SafeMIMEText,
    forbid_multi_line_headers, make_msgid,
)
#imports para pdf
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
#imports para reCAPTCHA
import urllib


class GenerateHTML(View):
	def get(self, request, *args, **kwargs):
		template = get_template('pdf/invoice.html')
		html = template.render(context)
		return html

def home(request):
	return render(request, 'home.html')

def preguntas(request):
	return render(request, 'preguntas.html')

def registro(request):
	context = {"form":RegistrationForm()}
	return render(request, 'registrate/register.html', context)

def addUser(request):
	form = RegistrationForm(request.POST)
	if form.is_valid():
		pass1 = request.POST['password']
		pass2 = request.POST['pass2']
		email = request.POST['email']
		username = request.POST['username']
		if Usuario.objects.filter(email = email).exists():
			messages.add_message(request, messages.ERROR, 'Este correo ya está registrado.', fail_silently=True,)
		else:
			if pass1 == pass2:
				if Usuario.objects.filter(username = username).exists():
					messages.add_message(request, messages.ERROR, 'Este alias está en uso.', fail_silently=True,)
				else:
					recaptcha_response = request.POST.get('g-recaptcha-response')
					url = 'https://www.google.com/recaptcha/api/siteverify'
					values = {
						'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
						'response': recaptcha_response
					}
					data = urllib.parse.urlencode(values).encode()
					req = urllib.request.Request(url, data = data)
					response = urllib.request.urlopen(req)
					result = json.loads(response.read().decode())
					if result['success']:
						registro = Usuario(is_superuser = False,
										   last_login = timezone.now(),
										   username = form.cleaned_data['username'],
										   first_name = form.cleaned_data['first_name'],
										   last_name = form.cleaned_data['last_name'],
										   email = form.cleaned_data['email'],
										   is_active = True,
										   genero = form.cleaned_data['genero'],
										   fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
										   password = make_password(pass1,salt=None, hasher='default'),
										   check_terminos = form.cleaned_data['check_terminos'],
										   foto = 'imagenes/perfil.jpg',
										   )
						registro.save()
						messages.add_message(request, messages.SUCCESS, 'Registro completado',fail_silently=True,)
					else:
						messages.add_message(request, messages.ERROR, 'No se ha podido completar el registo. Intentalo de nuevo', fail_silently=True,)
			else:
				messages.add_message(request, messages.ERROR, 'La contraseña no coninciden.', fail_silently=True,)
	return redirect('registro')


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			messages.add_message(request, messages.ERROR, 'El usuario o la contraseña son incorrectos.', fail_silently=True,)
			return redirect('login')
	context = {"form": LoginForm}
	return render(request, 'registrate/login.html', context)

def logout(request):
	auth.logout(request)
	return redirect('/')

def publicar(request):
	user = request.user
	form = TrayectoForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			registro = Trayecto(usuario = user,
								origen = request.POST['origen'],
								destino = request.POST['destino'],
								fecha_salida = request.POST['fecha_salida'],
								hora_recogida = request.POST['hora_recogida'],
								hora_llegada = request.POST['hora_llegada'],
								num_pasajeros = request.POST['num_pasajeros'],
								asiento_libre = request.POST['num_pasajeros'],
								precio_plaza = request.POST['precio_plaza'],
								check_carne = form.cleaned_data['check_carne'],
								)
			registro.save()
			messages.add_message(request, messages.SUCCESS, 'Tu trayecto se ha publicado correctamente.',fail_silently=True,)
	context = {'form':TrayectoForm, 'user': user}
	return render(request, 'trayectos/publicar_trayecto.html', context)


def terminosCondiciones(request):
	context = {'user': request.user}
	return render(request, 'terminosycondiciones.html', context)
def contacto(request):
	context = {'user': request.user, 'form':ContactoForm, }
	form = ContactoForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			mensaje =  request.POST['mensaje']
			registro = Mensaje(nombre = request.POST['nombre'],
								email = request.POST['email'],
								mensaje = request.POST['mensaje'],
								respondido = False
								)
			registro.save()
			messages.add_message(request, messages.SUCCESS, 'Tu mensaje ha sido enviado con exito.',fail_silently=True,)
	return render(request, 'contacto.html', context)

def sobreNosotros(request):
	return render(request, 'sobre-nosotros.html')

def perfil(request):
	user = request.user
	usuario = Usuario.objects.get(id=user.id)
	existe_coche = Vehiculo.objects.filter(usuario = user, activo = 1)
	coche = ''
	if existe_coche:
		coche = Vehiculo.objects.get(usuario = user, activo = 1)
	if request.method == 'GET':
		form = PersonalForm(instance = user)
	if request.method == 'POST':
		form = PersonalForm(request.POST)
		if form.is_valid():
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.fecha_nacimiento = request.POST['fecha_nacimiento']
			user.save()
			messages.add_message(request, messages.SUCCESS, 'Tu perfil se ha actualizado correctamente',fail_silently=True,)
	context = {'form': PasswordForm, 'user':   usuario, 'personal_form':form, 'cohe_form': CocheForm, 'coche':coche, 'foto_form':FotoForm}
	return render(request, 'usuario/perfil.html', context)

def changePassword(request):
	form = PasswordForm(request.POST)
	if form.is_valid():
		u = request.user
		password_actual = request.POST['password_actual']
		password_nueva = request.POST['password_nueva']
		password_confirma = request.POST['password_confirma']
		if u.check_password(password_actual) == True:
			if password_nueva == password_confirma:
				messages.add_message(request, messages.SUCCESS, 'Tu contraseña se ha cambiado con exito. Por favor vuelve a iniciar sesión',fail_silently=True,)
				u.set_password(password_nueva)
				print(u.set_password(password_nueva))
				u.save()
			else:
				messages.add_message(request, messages.ERROR, 'La contraseña que has introducido no coinciden.', fail_silently=True,)
				return redirect('perfil')
		else:
			messages.add_message(request, messages.ERROR, 'Las contraseñas introducida no es correcta', fail_silently=True,)
			return redirect('perfil')
	return redirect('login')

def addCoche(request):
	form = CocheForm(request.POST)
	if form.is_valid():
		user = request.user
		matricula = request.POST['matricula']
		expresion = '(\d{4})([A-Z]{3})'
		if bool(re.search(expresion, matricula)):
			registro = Vehiculo(
								matricula = matricula,
								modelo = form.cleaned_data['modelo'],
								usuario = user
								)
			registro.save()
			messages.add_message(request, messages.SUCCESS, 'Se ha añadido correctamente tu coche',fail_silently=True,)
		else:
			messages.add_message(request, messages.ERROR, 'Introduce una matricula correcta', fail_silently=True,)
	return redirect('perfil')

def deleteCoche(request, id):
	coche = Vehiculo.objects.get(id = id)
	coche.activo = 0
	coche.borrado = 1
	coche.save()
	messages.add_message(request, messages.SUCCESS, 'Se ha borrado correctamente tu coche',fail_silently=True,)
	return redirect('perfil')

def addFoto(request):
	user = request.user
	if request.method == 'POST':
		form = FotoForm(request.POST, request.FILES)
		if form.is_valid():
			user.foto = request.FILES['foto']
			user.save()
			messages.add_message(request, messages.SUCCESS, 'Se ha añadido correctamente tu foto',fail_silently=True,)
	return redirect('perfil')

def futurosViajes(request):
	date = datetime.now()
	viajes_publicados = Trayecto.objects.filter(fecha_salida__gte = date, activo = 1, usuario = request.user).order_by('fecha_salida', 'hora_recogida')
	reservas = Pago.objects.filter(comprador = request.user)
	context = {'viajes_publicados' : viajes_publicados, 'reservas':reservas,'user':request.user}
	return render(request, 'usuario/futuros-viajes.html', context)

def historial(request):
	date = datetime.now()
	viajes_publicados = Trayecto.objects.filter(fecha_salida__lte = date, activo = 1, usuario = request.user).order_by('fecha_salida')
	reservas = Pago.objects.filter(usuario = request.user )
	context = {'viajes_publicados' : viajes_publicados, 'reservas':reservas, 'user':request.user}
	return render(request, 'usuario/historial.html', context)

def buscar(request ):
	date = datetime.now()
	form = BuscarForm(request.POST)
	if request.method == 'GET':
		viajes = Trayecto.objects.filter(fecha_salida__gte = date, asiento_libre__gte = 1, activo = 1).order_by('fecha_salida', 'hora_recogida')
	if request.method == 'POST':
		if form.is_valid():
			origen = request.POST['origen']
			destino = request.POST['destino']
			fecha = request.POST['fecha']
			hora = request.POST['hora']
			viajes = Trayecto.objects.filter(origen = origen, destino = destino, fecha_salida = fecha, hora_recogida__gte = hora, asiento_libre__gte = 1,  activo = 1).order_by('fecha_salida', 'hora_recogida')
	context = {'viajes':viajes, 'form':form}
	return render(request, 'buscar.html', context)

def viaje(request, id):
	lista = []
	coche = None
	trayecto = Trayecto.objects.get(id=id)
	existe_coche = Vehiculo.objects.filter(usuario = trayecto.usuario, activo = 1)
	if existe_coche:
		coche = Vehiculo.objects.get(usuario = trayecto.usuario, activo = 1)
	for i in range(trayecto.asiento_libre):
		lista.append(i)
	context = {'trayecto': trayecto, 'coche':coche, 'lista':lista}
	return render(request, 'trayectos/viaje.html', context)

def pagar(request, id):
	trayecto = Trayecto.objects.get(id=id)
	coche = ''
	existe_coche = Vehiculo.objects.filter(usuario = trayecto.usuario, activo = 1)
	if existe_coche:
		coche = Vehiculo.objects.get(usuario = trayecto.usuario, activo = 1)
	context = {'trayecto':trayecto, 'coche':coche}
	return render(request, 'trayectos/checkout.html', context)

def detalles(request):
	date = datetime.now()
	user = request.user
	body = json.loads(request.body)
	trayecto = Trayecto.objects.get(id = body['productId'])
	print('hola 1')
	registro = Pago(
		destinatario = body['destinatario'],
		comprador = user,
		trayecto = trayecto,
		cantidad = body['cantidad'],
		fecha_pago = date,
		)
	print('hola 2')
	registro.save()
	plazas = trayecto.asiento_libre
	trayecto.asiento_libre = plazas - 1
	trayecto.save()
	print('hola 3')
	template = get_template('pdf/invoice.html')
	context = {
			"reserva_id":registro.id,
			"reserva_fecha": registro.fecha_pago,
			"nombre_cliente": registro.comprador.first_name,
			"origen": registro.trayecto.origen,
			"destino": registro.trayecto.destino,
			"fecha": registro.trayecto.fecha_salida,
			"precio": registro.cantidad,
	}
	print('hola 3')
	html = template.render(context)
	subject = 'Confirmación de reserva #'+ str(registro.id) +''
	message = 'Has reservado en Job&Car'
	from_email = settings.EMAIL_HOST_USER
	recipient_list =  [registro.comprador.email]
	print(registro.comprador.email)
	html_message = html
	mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
	mail.attach_alternative(html_message, 'text/html')
	mail.send()
	print('hola 4')
	return JsonResponse('Pago completado', safe = False)


def cartera(request):
	user = request.user
	id_user = user.id
	reservas = Pago.objects.filter(destinatario = id_user)
	context = {'reservas':reservas}
	return render(request, 'usuario/cartera.html', context)