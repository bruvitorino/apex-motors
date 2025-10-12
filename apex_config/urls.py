# Em apex_config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. A autenticação vem primeiro
    path('contas/', include('django.contrib.auth.urls')),
    
    # 2. A nossa app principal vem depois, capturando todo o resto
    path('', include('core.urls')),
]
