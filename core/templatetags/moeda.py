"""
Filtro customizado para formatação de valores monetários no padrão brasileiro
Arquivo: core/templatetags/moeda.py
"""

from django import template

register = template.Library()

@register.filter(name='moeda_br')
def moeda_br(valor):
    """
    Formata um valor numérico para o padrão monetário brasileiro.
    
    Exemplo:
        {{ veiculo.valor|moeda_br }}
        
    Entrada: 499000.00
    Saída: R$ 499.000,00
    """
    try:
        # Converte para float se necessário
        valor_float = float(valor)
        
        # Formata com 2 casas decimais
        valor_formatado = f"{valor_float:,.2f}"
        
        # Substitui vírgula e ponto (padrão americano → brasileiro)
        valor_formatado = valor_formatado.replace(',', 'X')  # Temporário
        valor_formatado = valor_formatado.replace('.', ',')  # Decimal
        valor_formatado = valor_formatado.replace('X', '.')  # Milhares
        
        return f"R$ {valor_formatado}"
    except (ValueError, TypeError):
        return valor