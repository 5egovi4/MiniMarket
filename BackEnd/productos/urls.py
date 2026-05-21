from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_productos),
    path('agregar/', views.agregar_producto),
    path('<int:id>/', views.obtener_producto),
    path('<int:id>/actualizar/', views.actualizar_producto),
    path('<int:id>/eliminar/', views.eliminar_producto),
]