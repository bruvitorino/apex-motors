# Em core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #página principal
    path('', views.home, name='home'),
    #Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    #Vendedores
    path('vendedores/adicionar/', views.cria_vendedor, name='cria_vendedor'),
    path('vendedores/<int:id>/editar/', views.edita_vendedor, name='edita_vendedor'),
    path('vendedores/<int:id>/excluir/', views.exclui_vendedor, name='exclui_vendedor'),
    path('vendedores/', views.lista_vendedores, name='lista_vendedores'),
    # Clientes
    path('clientes/adicionar/', views.cria_cliente, name='cria_cliente'),
    path('clientes/<int:id>/editar/', views.edita_cliente, name='edita_cliente'),
    path('clientes/<int:id>/excluir/', views.exclui_cliente, name='exclui_cliente'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    #Vendas
    path('vendas/adicionar/', views.cria_venda, name='cria_venda'),
    path('vendas/<int:id>/editar/', views.edita_venda, name='edita_venda'),
    path('vendas/<int:id>/excluir/', views.exclui_venda, name='exclui_venda'),
    path('vendas/', views.lista_vendas, name='lista_vendas'),
    #Exportação
    path('dashboard/exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('dashboard/exportar-excel/', views.exportar_excel, name='exportar_excel'),
]
