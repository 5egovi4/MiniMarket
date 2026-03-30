from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario),
    path('login/', views.login_usuario),
    path('<int:id>/', views.obtener_usuario),
    path('<int:id>/actualizar/', views.actualizar_usuario),
    path('<int:id>/eliminar/', views.eliminar_usuario),
]