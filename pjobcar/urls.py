from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
#importacion del fichero views
from appjobcar import views
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views 
from django.conf import settings
# el servicio de ficheros estáticos durante el desarrollo añadiendo las líneas siguientes.
from django.conf import settings
from django.conf.urls.static import static
#importacion para pasar parametros al html
from appjobcar.views import GenerateHTML

urlpatterns = [
	url(r'^$', views.home, name='home'),
	path('account/', include('django.contrib.auth.urls')),
	path('admin/', admin.site.urls, name='admin'),
	path('pdf/<int:id>', login_required(GenerateHTML.as_view()), name='pdf'),
	path('faqs/', views.preguntas, name='preguntas'),
	path('registro/', views.registro, name='registro'),
	path('login/', views.login, name='login'),
	path('register/', views.addUser, name='addUser'),
	path('logout/', login_required(views.logout), name="logout"),
	path('trayecto/publicar-trayecto', login_required(views.publicar), name='publicar'),
	path('terminos-y-condiciones', views.terminosCondiciones, name="terminos-condiciones"),
	path('contacto', views.contacto, name="contacto"),
	path('sobre-nosotros/', views.sobreNosotros, name='sobreNosotros'),
	path('perfil/', login_required(views.perfil), name='perfil'),
	path('change-password/', login_required(views.changePassword), name='changepassword'),
	path('perfil/coche', login_required(views.addCoche), name = 'addCoche'),
	path('perfil/coche/<int:id>', login_required(views.deleteCoche), name = 'deleteCoche'),
	path('perfil/foto', login_required(views.addFoto), name = 'addFoto'),
	path('futuros-viajes/', login_required(views.futurosViajes), name = 'futurosViajes'),
	path('historial/', login_required(views.historial), name = 'historial'),
	path('buscar/', login_required(views.buscar), name = 'buscar'),
	path('viaje/<int:id>', login_required(views.viaje), name='viaje'),
	path('checkout/<int:id>', login_required(views.pagar), name='pagar'),
	path('detalles/', login_required(views.detalles), name='detalles'),
	path('cartera/', login_required(views.cartera), name='cartera'),
] 

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)