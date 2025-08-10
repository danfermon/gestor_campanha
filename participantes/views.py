import datetime
import json
import os
from django.http import HttpResponse
from django.template import loader
from .models import Participantes
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
from .forms import ParticipanteForm
from cupons.models import Cupom
from django.shortcuts import render, get_object_or_404, redirect

import re

from utils.funcoes_cupom import parse_dados_cupom

from datetime import datetime

import ast

def login_participante(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            participante = Participantes.objects.get(email=email)
            if check_password(senha, participante.senha):
                # Autenticado com sucesso – salvar ID na sessão
                request.session['participante_id'] = participante.id
                return redirect('painel_participante')  # ou a página pós-login
            else:
                erro = "Senha incorreta."
        except Participantes.DoesNotExist:
            erro = "Participante não encontrado."

        return render(request, 'home_participantes.html', {'erro': erro})

    return render(request, 'home_participantes.html')


# -----------------------------------------------------------

def participante(request):
  template = loader.get_template('participante copy.html')
  return HttpResponse(template.render())

# ------------------------------------------

'''def cadastrar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_participante')
    else:
        form = ParticipanteForm()

    return render(request, 'cadastrar_participante.html', {'form': form})'''

def cadastrar_participante(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        dt_nasc = request.POST.get('dt_nasc')
        cpf = re.sub(r'\D', '', request.POST.get('cpf', ''))  # remove pontuação
        celular = re.sub(r'\D', '', request.POST.get('celular', ''))
        email = request.POST.get('email')
        uf = request.POST.get('uf')
        cidade = request.POST.get('cidade')
        cep = re.sub(r'\D', '', request.POST.get('cep', ''))
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        num = request.POST.get('num')
        senha = request.POST.get('senha')

        # Criptografa a senha
        senha_hash = make_password(senha)

        # Cria e salva o participante
        participante = Participantes(
            nome=nome,
            dt_nasc= datetime.strptime(dt_nasc, '%d/%m/%Y').date(),
            cpf=cpf,
            celular= '55' + celular,
            email=email,
            uf=uf,
            cidade=cidade,
            cep=cep,
            rua=rua,
            bairro=bairro,
            num=num,
            senha=senha_hash
        )
        participante.save()
        return redirect('login_participante')

    return render(request, 'cadastrar_participante.html')
#-------------------------------------------------------------------------------------


def painel_participante(request):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('login_participante')
    
    participante = Participantes.objects.get(id=participante_id)

    # filtrar cupons cadastrados para o participante 
    cupons_participante = Cupom.objects.filter(participante = participante_id)
    if cupons_participante == '':
        cupons_participante = 'False'

    context = {
        'cupons': cupons_participante,
        'participante': participante
    }
    
    template = loader.get_template('painel_participante.html')
    return HttpResponse(template.render(context, request))

def cupons_participante(request, id_cupom):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('login_participante')
    
    participante = Participantes.objects.get(id=participante_id)

    # filtrar cupons cadastrados para o participante 
    cupons_participante = Cupom.objects.filter(participante = participante_id)

    context = {
        'cupons': cupons_participante,
        'participante': participante
    }
    
    template = loader.get_template('cupom_detalhado.html')
    return HttpResponse(template.render(context, request))

def dados_cupom(request, id_cupom):
    cupom = Cupom.objects.get(id = id_cupom)
    template = loader.get_template('cupom_detalhado.html')
    context = {
        'cupom' : cupom
    }
    return HttpResponse(template.render(context, request))



def home_participantes(request):
    return render(request, 'home_participantes.html')

def como_participar(request):
    return render(request, 'como_participar.html')

def regulamento(request):
    return render(request, 'regulamento.html')

def FAQ(request):
    return render(request, 'FAQ.html')

def resultados(request):
    return render(request, 'resultados.html')

def editar_particip(request, id):
    participante = get_object_or_404(Participantes, id=id)

    if request.method == "POST":
        participante.nome = request.POST.get('nome')
        participante.celular = request.POST.get('celular')
        participante.email = request.POST.get('email')
        participante.save()

    # Recupera cupons do participante (após ou fora do POST)
    cupons_participante = Cupom.objects.filter(participante=participante)

    # Se não tiver cupons, define como False (opcional)
    if not cupons_participante.exists():
        cupons_participante = False

    context = {
        'cupons': cupons_participante,
        'participante': participante
    }

    return render(request, 'painel_participante.html', context)


def login_e_cadastro(request):
    # lógica da view
    return render(request, 'iframe_login_cadastro.html')

def iframe_login(request):
    # lógica da view
    return render(request, 'iframe_login.html')


#--------- PARTE DE EXTRAÇÃO DE VALIDAÇÃO DOS DADOS DO CUPOM --------------------------------

def area_cupom(request, id):
    cupom = get_object_or_404(Cupom, id=id)

    if cupom.tipo_documento == 'SAT-cfe':
        try:
            dados_json_dict =  json.dumps(cupom.dados_json)
        except Exception:
            dados_json_dict = {}

        cupom_sefaz = json.loads(dados_json_dict)
        print(cupom_sefaz)
        dados_json = cupom_sefaz['data'][0]
    
    if cupom.tipo_documento == 'NFC-e':
        cupom_sefaz = cupom.dados_json
        print(cupom_sefaz)
        dados_json = cupom_sefaz[0]
   
    

#--------------------------------------------------------------------------

    if cupom.tipo_documento == 'NF-e':
        # 1. Se não existe dados_json, evitar qualquer processamento
        if not cupom.dados_json:
            print("[AVISO] cupom.dados_json está vazio ou None.")
            cupom_sefaz = {}
        elif isinstance(cupom.dados_json, dict):
            cupom_sefaz = cupom.dados_json
        else:
            try:
                cupom_sefaz = json.loads(cupom.dados_json)
            except Exception as e:
                print(f"[ERRO] Falha ao converter JSON da NF-e: {e}")
                cupom_sefaz = {}

        # 2. Extrair dados
        if isinstance(cupom_sefaz, dict) and "data" in cupom_sefaz:
            try:
                dados_json = cupom_sefaz["data"][0]
            except (IndexError, TypeError):
                print("[AVISO] 'data' encontrado mas vazio ou mal formatado.")
                dados_json = {}
        else:
            dados_json = cupom_sefaz

        # 3. Log para depuração
        print("=== DEBUG NF-e ===")
        print("Tipo de cupom_sefaz:", type(cupom_sefaz))
        print("Cupom SEFAZ keys:", list(cupom_sefaz.keys()) if isinstance(cupom_sefaz, dict) else cupom_sefaz)
        print("Dados JSON enviados ao template:", dados_json)

 


#-----------------------------------------------------------------------------------

        
   

    try:
        dados_cupom_dict = ast.literal_eval(cupom.dados_cupom)
    except Exception:
        dados_cupom_dict = {}

    contexto = {
        'cupom': cupom,
        'dados_cupom': dados_cupom_dict,
        'dados_json': dados_json #json.loads(dados_json_dict),
    }
 
   

    return render(request, 'area_cupom.html', contexto)
   






    


    





