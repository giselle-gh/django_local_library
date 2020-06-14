from django import forms
from datetime import datetime
from .models import Usuario
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm2(forms.Form):
	username = forms.CharField(max_length = 150,
							   widget = forms.TextInput(attrs = {'class': 'form-control'}))
	first_name = forms.CharField(max_length=15, 
							 widget = forms.TextInput(attrs = {'class': 'form-control'}))
	last_name = forms.CharField(label='Apellidos', max_length = 100,
								widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.CharField(label='Email:', max_length = 100, 
							widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder':'ejemplo@email.com'}))
	CHOICES = [('Mujer','Mujer'),('Hombre','Hombre'), ('Prefiero no contestar', 'Prefiero no contestar')]
	genero = forms.CharField(label="Género", max_length = 15, 
							widget = forms.RadioSelect(choices=CHOICES, attrs = {'class':'form-check-input'}))
	fecha_nacimiento = forms.DateField(label='Fecha de nacimiento:', 
								widget= forms.DateInput(format = '%d-%m-%Y',attrs={'min':'01-01-1900', 'type':'date','class':'form-control', 'placeholder':'DD/MM/YY'}))
	password = forms.CharField(label = 'Contraseña', min_length = 8,
							widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	pass2 = forms.CharField(label = 'Repita Contraseña', min_length = 8,
							widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	check = forms.BooleanField(widget = forms.CheckboxInput(attrs = {'class': ' form-check-input'}))

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ['password', 'username', 'first_name', 'last_name', 'email', 'genero', 'fecha_nacimiento', 'check_terminos']
		widgets = {
					'password': forms.PasswordInput(attrs = {'class':'form-control', 'min':'8'}),
					'username': forms.TextInput(attrs = {'class': 'form-control'}),
					'first_name': forms.TextInput(attrs = {'class': 'form-control'}),
					'last_name': forms.TextInput(attrs = {'class': 'form-control'}),
					'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder':'ejemplo@email.com'}),
					'genero': forms.RadioSelect(attrs = {'class':'form-check-input'}),
					'fecha_nacimiento': forms.DateInput(format = '%d-%m-%Y',attrs={'min':'01-01-1900', 'type':'date','class':'form-control', 'placeholder':'DD/MM/YY'}),
					'check_terminos': forms.CheckboxInput(attrs = {'class': ' form-check-input'})
					}

class LoginForm(forms.Form):
	username = forms.CharField( max_length = 150, 
							widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Alias'}))
	password = forms.CharField( min_length = 5,
								widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Constraseña'}))
class TrayectoForm(forms.Form):
	date = datetime.now()
	fecha = date.strftime("%d-%m-%Y")
	origen = forms.CharField(max_length = 150,
							 widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Dirección de recogida'}))
	destino = forms.CharField(max_length = 150,
							  widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Dirección de destino'}))
	fecha_salida = forms.DateField(widget = forms.DateInput(format = '%d-%m-%Y', attrs = {'min': fecha,  'type':'date', 'class':'form-control', 'placeholder':'DD/MM/YY'}))
	hora_recogida = forms.TimeField(widget = forms.TimeInput(attrs = {'type':'time','class':'form-control'}))
	hora_llegada = forms.TimeField(widget = forms.TimeInput(attrs = {'type':'time','class':'form-control'}))
	num_pasajeros = forms.IntegerField(widget = forms.NumberInput(attrs = {'class':'form-control', 'min':'1','max':'7'}))
	precio_plaza = forms.FloatField(widget = forms.NumberInput(attrs = {'class':'form-control'}))
	check_carne = forms.BooleanField(widget = forms.CheckboxInput(attrs = {'class':'form-check-input'}))

class ContactoForm(forms.Form):
	nombre = forms.CharField(max_length=25,
							 widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Nombre'}))
	email = forms.CharField(max_length = 80,
							widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Email'}))
	mensaje = forms.CharField(max_length = 300,
							  widget = forms.Textarea(attrs = {'class':'form-control', 'placeholder':'Mensaje (máximo 300 carácteres)', 'rows':'3'}))

class PasswordForm(forms.Form):
	password_actual = forms.CharField(max_length = 150,
							   widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password_nueva = forms.CharField(max_length = 150,
									 widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password_confirma = forms.CharField(max_length = 150,
							   widget = forms.PasswordInput(attrs = {'class':'form-control'}))


class PersonalForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ['first_name', 'last_name', 'email', 'fecha_nacimiento']
		widgets = {
					'first_name': forms.TextInput(attrs = {'class': 'form-control'}),
					'last_name': forms.TextInput(attrs = {'class': 'form-control'}),
					'email': forms.TextInput(attrs = {'class': 'form-control'}),
					'fecha_nacimiento': forms.DateInput(attrs={'class':'form-control', 'placeholder':'DD/MM/YY'})
				  }


class CocheForm(forms.Form):
	matricula = forms.CharField(max_length = 7,
							 widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'ej. 5623HZD'}))
	modelo = forms.CharField(max_length = 20,
							 widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'ej. Seat Ibiza'}))

class FotoForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ['foto']
		widget = {
					'foto': forms.FileInput(attrs = {'type': 'file', 'class':'custom-file-input'})
				 }

class BuscarForm(forms.Form):
	origen = forms.CharField(max_length = 150,
							 widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'¿De dónde sales?'}))
	destino = forms.CharField(max_length = 150,
							  widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': '¿Dónde vas?'}))
	fecha = forms.DateField(widget = forms.DateInput(format = '%d-%m-%Y', 
							attrs = {'type':'date', 'class':'form-control'}))
	hora = forms.TimeField(widget = forms.TimeInput(attrs = {'type':'time','class':'form-control'}))