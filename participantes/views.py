from django.http import HttpResponse
from django.template import loader
from .models import Participantes
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
from .forms import ParticipanteForm
from cupons.models import Cupom
from django.shortcuts import render, get_object_or_404, redirect
from utils.funcoes import parse_dados_cupom


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

        return render(request, 'login_participante.html', {'erro': erro})

    return render(request, 'login_participante.html')


# -----------------------------------------------------------

def participante(request):
  template = loader.get_template('participante copy.html')
  return HttpResponse(template.render())

# ------------------------------------------

def cadastrar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_participante')
    else:
        form = ParticipanteForm()

    return render(request, 'cadastrar_participante.html', {'form': form})


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


#--------- PARTE DE EXTRAÇÃO DE VALIDAÇÃO DOS DADOS DO CUPOM --------------------------------


def area_cupom(request, id):
    cupom = get_object_or_404(Cupom, id=id)
    dados_ocr = parse_dados_cupom(cupom.dados_cupom or "")
    
    context = {
        'cupom': cupom,
        'dados_ocr': dados_ocr
    }
    return render(request, 'area_cupom.html', context)


