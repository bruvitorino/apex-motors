# Dentro de core/admin.py
from django.contrib import admin
from .models import Vendedor  # Importa o nosso novo modelo

# Registra o modelo Vendedor na interface de administração
admin.site.register(Vendedor)
