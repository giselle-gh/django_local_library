from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Usuario)
admin.site.register(Trayecto)
admin.site.register(Vehiculo)
admin.site.register(Pago)
admin.site.register(Mensaje)