from django import forms
from cupons.models.numero_sorte import NumeroDaSorte

class NumeroSorteForm(forms.ModelForm):
    class Meta:
        model = NumeroDaSorte
        fields = ['cupom', 'participante', 'numero', 'status']