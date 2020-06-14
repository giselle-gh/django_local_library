# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid
#Otras dependencias que se necesitan
import re
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin , BaseUserManager, AbstractUser
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now 
from datetime import date 

from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.db.models import signals
from django.db.models.fields import Field
#encriptacion de la contraseña
from passlib.hash import pbkdf2_sha256

class Usuario(AbstractUser):
	CHOICES = [('Mujer','Mujer'),('Hombre','Hombre'), ('PN', 'Prefiero no contestar')]
	genero = models.CharField(choices = CHOICES, max_length = 15, null = True, verbose_name=u"Género")
	fecha_nacimiento=models.DateField(null = True, verbose_name=u"Fecha Nacimiento")
	foto=models.ImageField(null = True, upload_to='imagenes', max_length=500, verbose_name=u"Foto")
	check_terminos = models.BooleanField(null = True, verbose_name=u"Acepta terminos")
	def verify_password(self, raw_password):
		return pbkdf2_sha256.verify(raw_password, self.password)

class Trayecto(models.Model):
	id = models.AutoField(primary_key=True, verbose_name=u"Id")
	usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name="Usuario")
	origen=models.CharField(max_length=80, verbose_name=u"Origen")
	destino=models.CharField(max_length=80, verbose_name=u"Destino")
	fecha_salida = models.DateField(verbose_name=u"Fecha")
	hora_recogida = models.TimeField(verbose_name=u"Hora recogida")
	hora_llegada = models.TimeField(verbose_name=u"Hora llegada")
	num_pasajeros = models.IntegerField(default=0,verbose_name=u"Num. Plazas")
	asiento_libre = models.IntegerField(default=0,verbose_name=u"Num. Plazas libres")
	precio_plaza = models.FloatField(max_length=4, verbose_name=u"Precio")
	check_carne = models.BooleanField(verbose_name=u"Carné conducir")
	activo = models.IntegerField(default = 1, verbose_name=u"Activo")
	borrado = models.IntegerField(default = 0, verbose_name=u"Borrado")
	def __str__(self):
		return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (self.id, self.usuario, self.origen, self.destino,self.fecha_salida, self.hora_recogida, self.num_pasajeros, self.asiento_libre, self.precio_plaza, self.check_carne)

class Pago(models.Model):
	id =  models.AutoField(primary_key=True, verbose_name=u"Id")
	destinatario = models.IntegerField(verbose_name=u"Destinatario")
	comprador = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name="comprador")
	trayecto = models.ForeignKey(Trayecto, on_delete = models.PROTECT, verbose_name = "Trayecto")
	cantidad = models.FloatField(max_length=4, verbose_name=u"Cantidad")
	fecha_pago = models.DateField(verbose_name=u"Fecha pago")
	def __str__(self):
		return'%s, %s, %s, %s, %s, %s' % (self.id, self.destinatario, self.comprador, self.trayecto, self.cantidad, self.fecha_pago)

class Vehiculo(models.Model):
	id=models.AutoField(primary_key=True, verbose_name=u"Id")
	matricula=models.CharField(max_length=7,verbose_name=u"Matricula")
	modelo=models.CharField(max_length=10,verbose_name=u"Modelo")
	usuario = models.ForeignKey(Usuario, null=True, on_delete=models.PROTECT, verbose_name=u"Id Usuario")
	activo = models.IntegerField(default=1,verbose_name=u"Activo")
	borrado = models.IntegerField(default=0,verbose_name=u"Borrado")
	def __str__(self):
		return '%s,%s,%s,%s,%s,%s' % (self.id,self.matricula,self.modelo,self.usuario, self.activo,self.borrado)

class Mensaje(models.Model):
	id = models.AutoField(primary_key = True, verbose_name=u"Id")
	nombre = models.CharField(max_length = 25, verbose_name=u"Nombre")
	email = models.CharField(max_length = 80, verbose_name=u"Email")
	mensaje = models.CharField(max_length = 300, verbose_name=u"Mensaje")
	respondido =  models.BooleanField(verbose_name=u"Respondido")
	def __str__(self):
		return '%s, %s, %s, %s' % (self.id, self.nombre, self.mensaje, self.respondido)