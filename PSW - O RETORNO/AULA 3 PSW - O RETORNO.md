# AULA 3 | PSW - O RETORNO

## Ver pet

Crie a URL ver pet:

```python
path('ver_pet/<int:id>', views.ver_pet, name="ver_pet"),
```

Crie a VIEW ver_pet:

```python
def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id = id)
        return render(request, 'ver_pet.html', {'pet': pet})
```

Crie o html ver_pet.html:

```python
{% load static %}
<!doctype html>
<html lang="pt-BR">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'usuarios/css/cadastro.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/novo_pet.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/seus_pet.css' %}" rel="stylesheet">
    <link href="{% static 'adotar/css/listar_pets.css' %}" rel="stylesheet">
    </head>
    <body>

        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 bg-side-plataforma sidebar">
                    <h2>ADO.TE</h2>
                    <hr>
                    
                    
                </div>

                <div style="padding:60px" class="col-md">
                    <h3 class="font-vinho">Informações do pet</h3>
                    <div class="row">
                        <div class="col-md-3">
                            <img width="100%" src="{{pet.foto.url}}">
                        </div>
                        <div class="col-md-9">
                            <span class="span-bold">Nome:</span>
                            <p>{{pet.nome}}</p>
                            <div style="width:40%">
                                
                            </div>
                        </div>
                    </div>  
                    <br>
                    <div class="row">
                        <div class="col-md-5"> 
                            <span class="span-bold">Descrição</span>
                            <p>{{pet.descricao}}</p>
                            
                        </div>

                        <div class="col-md-7">
                        </div>
                    </div>
                    <hr>

                    <div class="row">
                        <h3 class="font-vinho">Informações residenciais</h3>
                        <div class="col-md">
                            <div class="row">
                                <div class="col-md">
                                    <span class="span-bold">Estado</span>
                                    <p>{{pet.estado}}</p>
                                </div>

                                <div class="col-md">
                                    <span class="span-bold">Cidade</span>
                                    <p>{{pet.cidade}}</p>
                                </div>
                            </div>
                            <span class="span-bold">Telefone para contato</span>
                            <p>{{pet.telefone}}</p>
                            <br>
                            <a href="{% url 'pedido_adocao' pet.id %}" class="btn btn-success btn-lg">SOLICITAR ADOÇÃO</a>
                            
                        </div>

                        <div class="col-md">
                        </div>
                    </div>
                </div>

            </div>

            

        </div>

    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
</html>
```

Liste as tags:

```python
{% for tag in pet.tags.all%}
    <span class="badge text-bg-info badge-lg">{{tag}}</span>
{% endfor %}
```

Na listagem redirecione para URL criada:

```python
{% url 'ver_pet' pet.id %}
```

## Solicitar adoção

Crie a model para as solicitações de adoção:

```python
class PedidoAdocao(models.Model):
    choices_status = (
        ('AG', 'Aguardando aprovação'),
        ('AP', 'Aprovado'),
        ('R', 'Recusado')
    )

    pet = models.ForeignKey(Pet, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    status = models.CharField(max_length=2, choices=choices_status, default='AG')
```

FAÇA AS MIGRAÇÕES!

Crie a URL:

```python
path('pedido_adocao/<int:id_pet>', views.pedido_adocao, name="pedido_adocao"),
```

Crie a view pedido_adocao:

```python
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=request.user,
                          data=datetime.now())

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')
```

Faça as validações:

```python
if not pet.exists():
        messages.add_message(request, constants.ERROR, 'Esse pet já foi adotado :)')
        return redirect('/adotar')
```

No botão de solicitar adoção redirecione para URL criada:

```python
{% url 'pedido_adocao' pet.id %}
```

## Ver pedidos de adoção

No app divulgar crie a url:

```python
path('ver_pedido_adocao/', views.ver_pedido_adocao, name="ver_pedido_adocao"),
```

Crie a view ver_pedido_adocao:

```python
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})
```

Crie o html ver_pedido_adocao:

```python
{% load static %}
<!doctype html>
<html lang="pt-BR">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'usuarios/css/cadastro.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/novo_pet.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/seus_pet.css' %}" rel="stylesheet">
    <link href="{% static 'adotar/css/listar_pets.css' %}" rel="stylesheet">
    </head>
    <body>

        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 bg-side-plataforma sidebar">
                    <h2>ADO.TE</h2>
                    <hr>
                  
                    
                </div>

                <div style="padding:60px" class="col-md">
                    <div class="row">
                        {% if messages %}
                            <br>
                            {% for message in messages %}
                                <div class="alert {{message.tags}}">
                                    {{message}}
                                </div>
                            {% endfor %}
                        {% endif %}
                        {% for pedido in pedidos %}
                            <div class="col-md-3" style="margin-top: 20px;">
                                <div class="card" style="background-color: #D6D6D6; border:none;">
                                    <div style="padding:10px">
                                        <span clas="span-bold">{{pedido.pet.nome}}</span>
                                    </div>
                                    <img class="card-img-top" src="{{pedido.pet.foto.url}}">
                                    <div class="card-body">
                                        <h1 class="card-title">{{pedido.usuario.username}}</h1>
                                        <span class="span-bold2">Telefone:</span>
                                        <p>{{pedido.pet.telefone}}</p>
                                        
                                        <span class="span-bold2">Cidade:</span>
                                        <p>{{pedido.pet.cidade}}</p>
                                        <a href="" class="btn btn-success btn-lg">Aprovar</a>
                                        <a href="" class="btn btn-danger btn-lg">Recusar</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}

                        

                        
                        
                    </div>
                </div>

            </div>

            

        </div>

    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
</html>
```

Configure o envio de emails:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Crie a url:

```python
path('processa_pedido_adocao/<int:id_pedido>', views.processa_pedido_adocao, name="processa_pedido_adocao"),
```

Crie a view:

```python
from django.core.mail import send_mail
def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    if status == "A":
        pedido.status = 'AP'
        string = '''Olá, sua adoção foi aprovada. ...'''
    elif status == "R":
        string = '''Olá, sua adoção foi recusada. ...'''
        pedido.status = 'R'

    pedido.save()

    
    print(pedido.usuario.email)
    email = send_mail(
        'Sua adoção foi processada',
        string,
        'caio@pythonando.com.br',
        [pedido.usuario.email,],
    )
    
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso')
    return redirect('/divulgar/ver_pedido_adocao')
```

Em ver pedido de adoção redirecione para URL criada:

```python
<a href="{% url 'processa_pedido_adocao' pedido.id %}?status=A" class="btn btn-success btn-lg">Aprovar</a>
<a href="{% url 'processa_pedido_adocao' pedido.id %}?status=R" class="btn btn-danger btn-lg">Recusar</a>
```

## Dashboard

Crie a URL:

```python
path('dashboard/', views.dashboard, name="dashboard"),
```

Crie a view dashboard:

```python
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')
```

Crie o HTML:

```python
{% load static %}
<!doctype html>
<html lang="pt-BR">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'usuarios/css/cadastro.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/novo_pet.css' %}" rel="stylesheet">
    <link href="{% static 'divulgar/css/seus_pet.css' %}" rel="stylesheet">
    <link href="{% static 'adotar/css/listar_pets.css' %}" rel="stylesheet">
    </head>
    <body>

        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 bg-side sidebar">
                    <h2>ADO.TE</h2>
                    <hr>
                   
                    
                </div>

                <div style="padding:60px" class="col-md">

                    <h3 class="font-vinho">Quantidade de adoções por raça.</h3>
                     <div style="width: 60%;">
                        <canvas id="myChart"></canvas>
                    </div>  
                </div>

            </div>
        </div>

    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
</html>
```

Crie a URL:

```python
path('api_adocoes_por_raca/', views.api_adocoes_por_raca, name="api_adocoes_por_raca"),
```

Crie a VIEW:

```python
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)
```

Crie o JavaScript:

```python
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>

        fetch("/divulgar/api_adocoes_por_raca/",{
            method: 'GET',
        }).then(function(result){
            return result.json()
        }).then(function(data_adocoes){
           
            const data = {
                labels: data_adocoes['labels'],
                datasets: [{
                label: 'Peso paciente',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: data_adocoes['qtd_adocoes'],
                }]
            };

            const config = {
                type: 'line',
                data: data,
                options: {}
            };

            const myChart = new Chart(
                document.getElementById('myChart'),
                config
            );

        })

    </script>
```

## Python Full

Curso completo para te levar a sua primeira vaga como programador Python ainda em 2023.

Link para o PPC:

[https://pythonando.com.br/media/recursos_aulas/PLANEJAMENTO_PEDAGÓGICO.pdf](https://pythonando.com.br/media/recursos_aulas/PLANEJAMENTO_PEDAG%C3%93GICO.pdf)

## Leituras complementares

Vídeo enviar e-mails reais:

[https://www.youtube.com/watch?v=JSwofXOC4OY](https://www.youtube.com/watch?v=JSwofXOC4OY)

Artigo para configurar o GMAIL:

[https://medium.com/@heltonteixeira92/enviando-e-mail-com-django-e-uma-conta-gmail-atualizado-2022-bc2f186811ec](https://medium.com/@heltonteixeira92/enviando-e-mail-com-django-e-uma-conta-gmail-atualizado-2022-bc2f186811ec)