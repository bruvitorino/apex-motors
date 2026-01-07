# Conteúdo FINAL e CORRETO para: core/models.py

from django.db import models

# --- MODELO CONCESSIONARIA ---
class Concessionaria(models.Model):
    id_concessionarias = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, db_column='concessionaria')
    
    class Meta:
        managed = False
        db_table = 'concessionarias'

    def __str__(self):
        return self.nome

# --- MODELO VENDEDOR ---
class Vendedor(models.Model):
    id_vendedores = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    id_concessionarias = models.ForeignKey(Concessionaria, models.DO_NOTHING, db_column='id_concessionarias')
    data_inclusao = models.DateTimeField(blank=True, null=True)
    data_atualizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendedores'
    
    def __str__(self):
        return self.nome

# --- MODELO CLIENTE ---
class Cliente(models.Model):
    id_clientes = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, db_column='cliente')
    endereco = models.TextField(blank=True, null=True)
    id_concessionarias = models.ForeignKey(Concessionaria, models.DO_NOTHING, db_column='id_concessionarias')
    data_inclusao = models.DateTimeField(blank=True, null=True)
    data_atualizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'

    def __str__(self):
        return self.nome

# Em core/models.py

# ... (Concessionaria, Vendedor, Cliente continuam aqui em cima) ...


# --- MODELO VEICULO (ADAPTADO DO INSPECTDB) ---
class Veiculo(models.Model):
    id_veiculos = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_inclusao = models.DateTimeField(blank=True, null=True)
    data_atualizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'veiculos'

    def __str__(self):
        # Mostra o nome e o tipo para fácil identificação
        return f"{self.nome} ({self.tipo})"


# --- MODELO VENDA (ADAPTADO E CORRIGIDO) ---
class Venda(models.Model):
    id_vendas = models.IntegerField(primary_key=True)
    
    # Ajustamos os nomes das classes para o singular (como estão no nosso código)
    id_veiculos = models.ForeignKey(Veiculo, models.DO_NOTHING, db_column='id_veiculos')
    id_concessionarias = models.ForeignKey(Concessionaria, models.DO_NOTHING, db_column='id_concessionarias')
    id_vendedores = models.ForeignKey(Vendedor, models.DO_NOTHING, db_column='id_vendedores')
    id_clientes = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_clientes')
    
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField()
    data_inclusao = models.DateTimeField(blank=True, null=True)
    data_atualizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendas'

    def __str__(self):
        # Uma representação útil para a venda
        return f"Venda #{self.id_vendas} - Cliente: {self.id_clientes.nome}"
