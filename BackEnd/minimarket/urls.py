from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/productos/', include('productos.urls')),
    path('api/carrito/', include('carrito.urls')),
    path('api/pago/', include('pagos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)