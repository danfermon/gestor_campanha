from django.http import HttpResponse
from django.template import loader
from .models import Usuarios
from participantes.models import Participantes
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps
from utils.funcoes import limpar_lista_sku, retorna_atividades
from cupons.models import Cupom
from utils.link_sefaz import gerar_link_sefaz
## Função para restringir acessos por niveis - Danny - 27-06-2025
def nivel_required(nivel_permitido):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.nivel == nivel_permitido:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Acesso não autorizado")
        return _wrapped_view
    return decorator


## Função para restringir acesso apenas para administradores - Danny - 27-06-2025
def is_admin(user):
    return user.nivel == 'admin'

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())
  

@login_required
##@nivel_required('admin')
def cadastro(request):
  # salvar os dados da tela para o banco de dados
  if request.method == "GET": 
    return render(request, 'cadastro.html')
  elif request.method == "POST":
    nome = request.POST.get('nome')
    usr = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    #hashed_password = make_password(password=str(senha), salt='xxsaw21', hasher='pbkdf2_sha256')

    status = request.POST.get('status')
    ativo = True if status == "1" or status.lower() == "ativo" else False
    
    nivel = request.POST.get('nivel')
    if (nivel != '1') or (nivel != '2') or (nivel != '3'):
       nivel = 0

    

    #avatar = request.POST.get('avatar_escolhido')
    #avatar_selecionado =  '/statc/avatar/' + avatar


    novo_usuario = Usuarios.objects.create_user(username = usr, 
                                                password = senha, 
                                                last_login = date.today(),
                                                is_superuser = False,
                                                is_staff = False,
                                                first_name = nome,
                                                email = email,
                                                is_active = ativo,
                                                nivel = nivel)
                                                #foto = avatar_selecionado)

    novo_usuario.save()
    return redirect('usuarios')
  
@login_required(login_url='login')
def sistema(request):
  current_user = request.user

  nivel_logado = current_user.nivel
  atividades = retorna_atividades(nivel_logado)

  context = {
    'usuario': current_user,
    'atividades_usuario': atividades
  }


  template = loader.get_template('sistema.html')
  return HttpResponse(template.render(context, request))

@login_required
def usuarios(request):
  usuarios = Usuarios.objects.all().values()
  template = loader.get_template('todos_usuarios.html')
  context = {
    'usuarios': usuarios,
  }
  return HttpResponse(template.render(context, request))

# dash
@login_required
def dash(request):
  template = loader.get_template('dash.html')
  return HttpResponse(template.render())

@login_required
def relatorios(request):
  template = loader.get_template('relatorios.html')
  return HttpResponse(template.render())


# Detalhamento de usuarios
@login_required
def detalhe(request, id):
  usuario = Usuarios.objects.get(id=id)
  template = loader.get_template('detalhe.html')
  context = {
    'usuarios': usuario,
  }
  return HttpResponse(template.render(context, request))

# Deletar usuarios
@login_required
def deletar(request, id):
  usuario = Usuarios.objects.get(id=id)
  usuario.delete()
  return redirect('usuarios')

# Editar usuarios
@login_required
def editar(request, id):
  if request.method == "GET": 
    return render(request, 'usuarios.html')
  elif request.method == "POST":
    usuario = Usuarios.objects.get(id=id)
    usr = request.POST.get('usuario')
    email = request.POST.get('email')
    
    status = request.POST.get('status')
    ativo = True if status == "1" or status.lower() == "ativo" else False

    nivel = request.POST.get('nivel')

    usuario.username = usr 
    usuario.email = email
    usuario.is_active = ativo
    usuario.nivel = nivel
    
    usuario.save()
    return redirect('usuarios')

# Editar perfil do usuarios
@login_required
def perfil(request, id):
  if request.method == "GET": 
    return render(request, 'sistema.html')
  elif request.method == "POST":

    usuario = Usuarios.objects.get(id=id)

    nome  = request.POST.get('nome')
    usr   = request.POST.get('usuario')
    email = request.POST.get('email')
    
    senha = request.POST.get('senha')
    if senha != '*******':
      usuario.password = make_password(senha)

    usuario.first_name = nome
    usuario.username = usr 
    usuario.email = email
    
    usuario.save()
    return redirect('sistema')
  


@login_required
def dados_participantes(request):
  #pegar os dados dos participantes
  lista_participantes = Participantes.objects.all().values()
  template = loader.get_template('dados_participantes.html')
  context = {
    'lista_participantes': lista_participantes,
  }
  return HttpResponse(template.render(context, request))


@login_required
def sorteios(request):
  template = loader.get_template('sorteios.html')
  return HttpResponse(template.render())


# Editar Participantes
@login_required
def editar_participante(request, id):
  if request.method == "GET": 
    return render(request, 'dados_participantes.html')
  elif request.method == "POST":
    participante = Participantes.objects.get(id=id)
    nome    =  request.POST.get('nome')
    celular = request.POST.get('celular')
    email   = request.POST.get('email')
    status  = request.POST.get('status')
    
    participante.nome     = nome 
    participante.celular  = celular
    participante.email    = email
    participante.status   = status
    
    participante.save()
    return redirect('dados_participantes')


# Detalhamento de participante
@login_required
def participante_detalhado(request, id):
  participante = Participantes.objects.get(id=id)
  template = loader.get_template('participante_detalhado.html')
  context = {
    'participante': participante,
  }
  return HttpResponse(template.render(context, request))


# Pesquisar participante por nome ou por cpf
@login_required
def pesquisar_participante(request):
  if request.method == "GET": 
    template = loader.get_template('pesquisar_participante.html')
    context = {
      'participante': '',
    }
    return HttpResponse(template.render(context, request))
    
  elif request.method == "POST":
    texto = request.POST.get('texto')
    
    try:
      participante = Participantes.objects.get(cpf=texto) 
      template = loader.get_template('pesquisar_participante.html')
      context = {
        'participante': participante,
       
      }
      return HttpResponse(template.render(context, request))
    
    except Participantes.DoesNotExist:
       template = loader.get_template('pesquisar_participante.html')
       context = {
        'mensagem': 'Não houve retorno para essa pesquisa. Tente usar outro parâmetro'
       }
       return HttpResponse(template.render(context, request))


def deletar_skus(request):
  current_user = request.user
  nivel_logado = current_user.nivel
  atividades = retorna_atividades(nivel_logado)


  if current_user.is_superuser == 1:
    try:
      msg = limpar_lista_sku('skus_validos') 
    except:
      msg = 'Não foi possível limpara a lista - Consultar a equipe de desenvolvimento'
    
    context = {
      'usuario': current_user,
      'atividades_usuario': atividades,
      'msg_sku' : msg
    }
    template = loader.get_template('sistema.html')
    return HttpResponse(template.render(context, request))
  
  else:
    msg = 'Usuário não altorizado a fazer essa ação!'
    context = {
      'usuario': current_user,
      'atividades_usuario': atividades,
      'msg_sku' : msg
    }
    template = loader.get_template('sistema.html')
    return HttpResponse(template.render(context, request))


@login_required
def cupons_enviados(request):
  # filtrar cupons cadastrados
  lista_cupons = Cupom.objects.all().values()
  total_cup = Cupom.objects.count()
  template = loader.get_template('cupons_enviados.html')
  context = {
    'lista_cupons': lista_cupons,
    'Total' : total_cup
  }
  return HttpResponse(template.render(context, request))
  


   

    

