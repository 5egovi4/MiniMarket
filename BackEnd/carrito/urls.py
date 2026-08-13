from django.urls import path
from . import views

urlpatterns =[
    path('agregar_producto/', views.agregar_producto),
    path('<int:id>/ver_carrito/', views.ver_carrito),
    path('<int:id_usuario>/eliminar_producto/<int:id_producto>/', views.eliminar_producto),
    path('<int:id_usuario>/vaciar_carrito/', views.vaciar_carrito),
    path('<int:id_usuario>/total/', views.obtener_total)
]