# Conteúdo FINAL, LIMPO e CORRETO para: core/views.py

# --- 1. IMPORTAÇÕES ---
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import Vendedor, Concessionaria, Cliente, Veiculo, Venda

# ==================
# --- VENDEDORES ---
# ==================

@login_required
def lista_vendedores(request):
    vendedores = Vendedor.objects.all().order_by('id_vendedores')
    context = {'vendedores': vendedores}
    return render(request, 'core/lista_vendedores.html', context)

@login_required
def cria_vendedor(request):
    if request.method == 'POST':
        nome_vendedor = request.POST.get('nome')
        id_concessionaria = request.POST.get('id_concessionaria')
        max_id_result = Vendedor.objects.aggregate(max_id=Max('id_vendedores'))
        max_id = max_id_result['max_id'] if max_id_result['max_id'] is not None else 0
        next_id = max_id + 1
        now = timezone.now()
        Vendedor.objects.create(
            id_vendedores=next_id, nome=nome_vendedor, id_concessionarias_id=id_concessionaria,
            data_inclusao=now, data_atualizacao=now
        )
        return redirect('lista_vendedores')
    concessionarias = Concessionaria.objects.all().order_by('nome')
    context = {'concessionarias': concessionarias}
    return render(request, 'core/form_vendedor.html', context)

@login_required
def edita_vendedor(request, id):
    vendedor = Vendedor.objects.get(id_vendedores=id)
    if request.method == 'POST':
        vendedor.nome = request.POST.get('nome')
        vendedor.id_concessionarias_id = request.POST.get('id_concessionaria')
        vendedor.data_atualizacao = timezone.now()
        vendedor.save()
        return redirect('lista_vendedores')
    concessionarias = Concessionaria.objects.all().order_by('nome')
    context = {'vendedor': vendedor, 'concessionarias': concessionarias}
    return render(request, 'core/form_edita_vendedor.html', context)

@login_required
def exclui_vendedor(request, id):
    vendedor = Vendedor.objects.get(id_vendedores=id)
    if request.method == 'POST':
        vendedor.delete()
        return redirect('lista_vendedores')
    context = {'vendedor': vendedor}
    return render(request, 'core/confirma_exclusao.html', context)


# ==================
# --- CLIENTES ---
# ==================
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id_clientes')
    context = {'clientes': clientes}
    return render(request, 'core/lista_clientes.html', context)

# --- VERSÃO CORRIGIDA DA CRIA_CLIENTE ---
@login_required
def cria_cliente(request):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome')
        endereco_cliente = request.POST.get('endereco')
        id_concessionaria = request.POST.get('id_concessionaria')
        max_id_result = Cliente.objects.aggregate(max_id=Max('id_clientes'))
        max_id = max_id_result['max_id'] if max_id_result['max_id'] is not None else 0
        next_id = max_id + 1
        now = timezone.now()
        Cliente.objects.create(
            id_clientes=next_id, nome=nome_cliente, endereco=endereco_cliente,
            id_concessionarias_id=id_concessionaria, data_inclusao=now, data_atualizacao=now
        )
        return redirect('lista_clientes')
    
    # Esta parte agora está corretamente alinhada com o 'if'
    concessionarias = Concessionaria.objects.all().order_by('nome')
    context = {'concessionarias': concessionarias}
    return render(request, 'core/form_cliente.html', context)

@login_required
def edita_cliente(request, id):
    # Busca o cliente específico que queremos editar
    cliente = Cliente.objects.get(id_clientes=id)
    
    # Se o formulário foi enviado (método POST)
    if request.method == 'POST':
        # Pega os dados do formulário
        cliente.nome = request.POST.get('nome')
        cliente.endereco = request.POST.get('endereco')
        cliente.id_concessionarias_id = request.POST.get('id_concessionaria')
        
        # Atualiza a data de modificação
        cliente.data_atualizacao = timezone.now()
        
        # Salva as alterações no banco de dados
        cliente.save()
        
        # Redireciona para a lista de clientes
        return redirect('lista_clientes')

    # Se a requisição for GET (primeira vez que a página é carregada)
    
    # Busca a lista de concessionárias para o dropdown
    concessionarias = Concessionaria.objects.all().order_by('nome')
    
    # Cria o contexto com o cliente e a lista de concessionárias
    context = {
        'cliente': cliente,
        'concessionarias': concessionarias
    }
    
    # Renderiza o template do formulário de edição
    return render(request, 'core/form_edita_cliente.html', context)

@login_required
def exclui_cliente(request, id):
    # Busca o cliente que queremos deletar
    cliente = Cliente.objects.get(id_clientes=id)

    # Se a requisição for POST, o usuário confirmou a exclusão
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    # Se a requisição for GET, mostramos a página de confirmação
    context = {
        'cliente': cliente
    }
    # Aponta para um novo template de confirmação
    return render(request, 'core/confirma_exclusao_cliente.html', context)

# ==================
# --- VENDAS ---
# ==================
@login_required
def lista_vendas(request):
    # .select_related() é uma otimização para buscar os dados das ForeignKeys
    # de uma só vez, evitando múltiplas consultas ao banco.
    vendas = Venda.objects.select_related(
        'id_clientes', 'id_vendedores', 'id_veiculos'
    ).all().order_by('-id_vendas') # Ordena pelas mais recentes primeiro

    context = {
        'vendas': vendas
    }
    return render(request, 'core/lista_vendas.html', context)

@login_required
def cria_venda(request):
    # --- LÓGICA DO POST (quando o formulário é enviado) ---
    if request.method == 'POST':
        # 1. Pega os dados dos dropdowns e campos
        id_cliente = request.POST.get('id_cliente')
        id_veiculo = request.POST.get('id_veiculo')
        id_vendedor = request.POST.get('id_vendedor')
        id_concessionaria = request.POST.get('id_concessionaria')
        valor_pago = request.POST.get('valor_pago')
        data_venda = request.POST.get('data_venda')

        # 2. Calcula o próximo ID da venda
        max_id_result = Venda.objects.aggregate(max_id=Max('id_vendas'))
        max_id = max_id_result['max_id'] if max_id_result['max_id'] is not None else 0
        next_id = max_id + 1

        # 3. Pega a data e hora atuais para os campos de controle
        now = timezone.now()

        # 4. Cria a nova venda no banco de dados
        Venda.objects.create(
            id_vendas=next_id,
            id_clientes_id=id_cliente,
            id_veiculos_id=id_veiculo,
            id_vendedores_id=id_vendedor,
            id_concessionarias_id=id_concessionaria,
            valor_pago=valor_pago,
            data_venda=data_venda,
            data_inclusao=now,
            data_atualizacao=now
        )

        # 5. Redireciona para a lista de vendas
        return redirect('lista_vendas')

    # --- LÓGICA DO GET (quando a página é carregada) ---
    # Busca todas as listas necessárias para os dropdowns
    clientes = Cliente.objects.all().order_by('nome')
    vendedores = Vendedor.objects.all().order_by('nome')
    veiculos = Veiculo.objects.all().order_by('nome')
    concessionarias = Concessionaria.objects.all().order_by('nome')
    
    context = {
        'clientes': clientes,
        'vendedores': vendedores,
        'veiculos': veiculos,
        'concessionarias': concessionarias
    }
    # Aponta para o novo template de formulário de venda
    return render(request, 'core/form_venda.html', context)

@login_required
def edita_venda(request, id):
    # Busca a venda específica que queremos editar
    venda = Venda.objects.get(id_vendas=id)
    
    # Se o formulário foi enviado (método POST)
    if request.method == 'POST':
        # Atualiza os campos da venda com os dados do formulário
        venda.id_clientes_id = request.POST.get('id_cliente')
        venda.id_veiculos_id = request.POST.get('id_veiculo')
        venda.id_vendedores_id = request.POST.get('id_vendedor')
        venda.id_concessionarias_id = request.POST.get('id_concessionaria')
        venda.valor_pago = request.POST.get('valor_pago')
        venda.data_venda = request.POST.get('data_venda')
        
        # Atualiza a data de modificação
        venda.data_atualizacao = timezone.now()
        
        # Salva as alterações no banco de dados
        venda.save()
        
        # Redireciona para a lista de vendas
        return redirect('lista_vendas')

    # Se a requisição for GET (primeira vez que a página é carregada)
    
    # Busca todas as listas para os dropdowns
    clientes = Cliente.objects.all().order_by('nome')
    vendedores = Vendedor.objects.all().order_by('nome')
    veiculos = Veiculo.objects.all().order_by('nome')
    concessionarias = Concessionaria.objects.all().order_by('nome')
    
    # Cria o contexto com a venda e todas as listas
    context = {
        'venda': venda,
        'clientes': clientes,
        'vendedores': vendedores,
        'veiculos': veiculos,
        'concessionarias': concessionarias
    }
    
    # Renderiza o template do formulário de edição
    return render(request, 'core/form_edita_venda.html', context)

@login_required
def exclui_venda(request, id):
    # Busca a venda que queremos deletar
    venda = Venda.objects.get(id_vendas=id)

    # Se a requisição for POST, o usuário confirmou a exclusão
    if request.method == 'POST':
        venda.delete()
        return redirect('lista_vendas')

    # Se a requisição for GET, mostramos a página de confirmação
    context = {
        'venda': venda
    }
    # Aponta para o novo template de confirmação
    return render(request, 'core/confirma_exclusao_venda.html', context)

# Em core/views.py

# ... (todas as outras views ficam aqui em cima) ...

# ===============================================
# --- 5. VIEWS PARA O SITE PÚBLICO ---
# ===============================================

# Esta view NÃO precisa de @login_required
def home(request):
    # Busca todos os veículos no banco de dados, ordenados pelo nome
    veiculos = Veiculo.objects.all().order_by('nome')
    
    # Prepara o contexto para enviar os dados para o template
    context = {
        'veiculos': veiculos
    }
    
    # Renderiza um novo template que vamos criar
    return render(request, 'core/home.html', context)
