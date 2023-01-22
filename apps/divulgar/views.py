from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from apps.adotar.models import PedidoAdocao
from django.http import JsonResponse 
from django.contrib import messages
from .models import Tag, Raca, Pet

@login_required(login_url='/auth/login/')
def novo_pet(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags':tags, 'racas':racas})
    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        print(tag.id for tag in Tag.objects.all() if tag in tags)
        print([tag.id for tag in Tag.objects.all()])

        pet = Pet(usuario=request.user, foto=foto, nome=nome, descricao=descricao, estado=estado, cidade=cidade, telefone=telefone, raca_id=raca)
        pet.save()
        ([pet.tags.add(Tag.objects.get(id=tag_id)) for tag_id in tags])
        pet.save()
        return redirect('/divulgar/novo_pet/')

@login_required(login_url='/auth/login/')
def seus_pets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets':pets})
    
@login_required(login_url='/auth/login')
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)
    if not pet.usuario == request.user:
        messages.error(request, 'Esse pet não é seu')
        return redirect('/divulgar/seus_pets/')
    pet.delete()
    messages.success(request, 'Pet removido com sucesso')
    return redirect('/divulgar/seus_pets/')

def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})
    
@csrf_exempt    
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()
    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)
    racas = [raca.raca for raca in racas]
    data = {
        'qtd_adocoes': qtd_adocoes,
        'labels': racas
    }
    return JsonResponse(data)
