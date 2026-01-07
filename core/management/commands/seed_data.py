"""
Management command para popular o banco de dados do Apex Motors
Arquivo: core/management/commands/seed_data.py
"""

from django.core.management.base import BaseCommand
from django.db import connection
from datetime import datetime


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais do Apex Motors'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando seed do banco de dados...'))
        
        try:
            # Criar tabelas manualmente (já que managed=False)
            self.criar_tabelas()
            
            # Popular com dados
            self.popular_veiculos()
            
            self.stdout.write(self.style.SUCCESS('✅ Seed concluído com sucesso!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro no seed: {e}'))
            raise

    def criar_tabelas(self):
        """Cria as tabelas necessárias"""
        self.stdout.write('📊 Criando tabelas...')
        
        with connection.cursor() as cursor:
            # Tabela concessionarias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS concessionarias (
                    id_concessionarias INTEGER PRIMARY KEY,
                    concessionaria VARCHAR(255) NOT NULL
                );
            """)
            
            # Tabela vendedores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendedores (
                    id_vendedores INTEGER PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    id_concessionarias INTEGER,
                    data_inclusao TIMESTAMP,
                    data_atualizacao TIMESTAMP,
                    FOREIGN KEY (id_concessionarias) REFERENCES concessionarias(id_concessionarias)
                );
            """)
            
            # Tabela clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_clientes INTEGER PRIMARY KEY,
                    cliente VARCHAR(255) NOT NULL,
                    endereco TEXT,
                    id_concessionarias INTEGER,
                    data_inclusao TIMESTAMP,
                    data_atualizacao TIMESTAMP,
                    FOREIGN KEY (id_concessionarias) REFERENCES concessionarias(id_concessionarias)
                );
            """)
            
            # Tabela veiculos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS veiculos (
                    id_veiculos INTEGER PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    tipo VARCHAR(100) NOT NULL,
                    valor DECIMAL(10, 2) NOT NULL,
                    data_inclusao TIMESTAMP,
                    data_atualizacao TIMESTAMP
                );
            """)
            
            # Tabela vendas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id_vendas INTEGER PRIMARY KEY,
                    id_veiculos INTEGER,
                    id_concessionarias INTEGER,
                    id_vendedores INTEGER,
                    id_clientes INTEGER,
                    valor_pago DECIMAL(10, 2) NOT NULL,
                    data_venda TIMESTAMP NOT NULL,
                    data_inclusao TIMESTAMP,
                    data_atualizacao TIMESTAMP,
                    FOREIGN KEY (id_veiculos) REFERENCES veiculos(id_veiculos),
                    FOREIGN KEY (id_concessionarias) REFERENCES concessionarias(id_concessionarias),
                    FOREIGN KEY (id_vendedores) REFERENCES vendedores(id_vendedores),
                    FOREIGN KEY (id_clientes) REFERENCES clientes(id_clientes)
                );
            """)
            
        self.stdout.write(self.style.SUCCESS('  ✅ Tabelas criadas'))

    def popular_veiculos(self):
        """Popula a tabela de veículos com os 7 modelos da Apex Motors"""
        self.stdout.write('🚗 Populando veículos...')
        
        veiculos = [
            (1, 'Apex Neo', 'Hatchback Popular', 89000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (2, 'Apex Verso', 'MPV Familiar', 119000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (3, 'Apex Stratos', 'SUV Urbano/Aventura', 159000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (4, 'Apex Orion', 'Sedã Executivo', 179000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (5, 'Apex Titan', 'Caminhonete Robusta', 269000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (6, 'Apex Vortex', 'Supercar Esportivo', 459000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
            (7, 'Apex Ion', 'Sedã Elétrico Premium', 499000.00, '2023-01-15 08:00:00', '2023-01-15 08:00:00'),
        ]
        
        with connection.cursor() as cursor:
            # Verifica se já existem veículos
            cursor.execute("SELECT COUNT(*) FROM veiculos")
            count = cursor.fetchone()[0]
            
            if count > 0:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Já existem {count} veículos no banco. Pulando...'))
                return
            
            # Insere os veículos
            for veiculo in veiculos:
                cursor.execute("""
                    INSERT INTO veiculos 
                    (id_veiculos, nome, tipo, valor, data_inclusao, data_atualizacao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, veiculo)
            
        self.stdout.write(self.style.SUCCESS(f'  ✅ {len(veiculos)} veículos inseridos'))
