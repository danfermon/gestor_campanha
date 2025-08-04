# campanha/forms.py
from django import forms
from .models import Participantes
from django.contrib.auth.hashers import make_password
#from utils.funcoes import validar_cep  # se quiser validar o cep no back-end também

class ParticipanteForm(forms.ModelForm):
    senhaconf = forms.CharField(widget=forms.PasswordInput(), label='Confirme a Senha')
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha')

    class Meta:
        model = Participantes
        fields = ['nome', 'dt_nasc', 'cpf','celular', 'email',
                  'uf', 'cidade', 'cep', 'rua', 'bairro', 'num', 'senha']

    def clean_CEP(self):
        cep = self.cleaned_data.get("CEP")
        # if not validar_cep(cep):  # opcional
        #     raise forms.ValidationError("CEP inválido ou não encontrado.")
        return cep

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senhaconf = cleaned_data.get("senhaconf")

        if senha and senhaconf and senha != senhaconf:
            raise forms.ValidationError("As senhas não coincidem.")

        cleaned_data['senha'] = make_password(senha)
        return cleaned_data