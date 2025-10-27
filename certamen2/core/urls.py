from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #paginas principales
    path('', views.index, name='index'),    
    path('eventos/', views.eventos, name='eventos'), 

    # usuarios no registrados
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', next_page='eventos'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # usuarios registrados
    path('inscribir/<int:evento_id>/', views.inscribirse, name='inscribirse'), 
    path('mi_cuenta/', views.mi_cuenta, name='mi_cuenta'), 
    path('mi-cuenta/anular/<int:inscripcion_id>/', views.anular_inscripcion, name='anular_inscripcion'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
