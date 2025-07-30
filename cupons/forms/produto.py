from django import forms
from cupons.models.produto import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['cupom', 'nome', 'quantidade', 'valor_unitario']

