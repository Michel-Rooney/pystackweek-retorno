from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .utils import cadastro_is_valid
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet/')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not cadastro_is_valid(request, nome, email, senha, confirmar_senha):
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()
            messages.success(request, 'Usuário criado com sucesso')
        except:
            messages.error(request, 'Não foi possível criar um usuário')
        return redirect('/auth/cadastro')
    
def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet/')
        return render(request, 'login.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = auth.authenticate(username=nome, password=senha)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Usuário logado com sucesso')
            return redirect('/divulgar/novo_pet/')
        else:
            messages.error(request, 'Não foi possível fazer o login')
            return redirect('/auth/login')
        
def sair(request):
    auth.logout(request)
    messages.success(request, 'Usuario deslogado com sucesso')
    return redirect('/auth/login')

