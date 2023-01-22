from django.shortcuts import render, redirect
from apps.divulgar.models import Pet, Raca
from django.core.mail import send_mail
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime

def listar_pets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()
        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')
        if cidade:
            pets = pets.filter(cidade__icontains=cidade)
        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)
        return render(request, 'listar_pets.html', {'pets':pets, 'racas':racas, 'cidade':cidade, 'raca_filtro':raca_filter})

def ver_pet(request, id):
    if request.method == 'GET':
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet':pet})
    
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")
    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=request.user,
                          data=datetime.now())
    pedido.save()
    messages.success(request, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')
    
def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    match status:
        case 'A':
            pedido.status = 'AP'
            string = '''Olá, sua adoção foi aprovada.'''
        case 'R':
            pedido.status = 'R'
            string = '''Olá, sua adoção foi recusasa'''
    pedido.save()
    email = send_mail('Sua adoção foi processada', string, 'email@email.com', [pedido.usuario.email])
    messages.success(request, 'Pedido de adoção processado com sucesso')
    return redirect('/divulgar/ver_pedido_adocao/')

def dashboard(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')
