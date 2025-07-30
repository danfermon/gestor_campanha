from django import forms
from cupons.models.cupom import Cupom


class CupomForm(forms.ModelForm):
    class Meta:
        model = Cupom
        fields = [
            'participante',
            'nome_loja',
            'cnpj_loja',
            'tipo_documento',
            'numero_documento',
            'imagem_cupom',
            'valor_total',
            'tipo_envio',
            'status'
        ]
