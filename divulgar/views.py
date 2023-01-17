from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Tag, Raca, Pet
from adotar.models import PedidoAdocao
from django.contrib import messages
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt


@login_required
def novo_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        racas = Raca.objects.all()

        context = {
            'tags' : tags,
            'racas' : racas,
        }

        return render(request, 'novo_pet.html', context)

    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        # validar dados
        # api correios
        # messages error

        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,# salvando o id da raça
        )

        pet.save()
        
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)

        pet.save()
        tags = Tag.objects.all()
        racas = Raca.objects.all()

        context = {
            'tags' : tags,
            'racas' : racas,
        }

        messages.add_message(request, constants.SUCCESS, 'Novo pet cadastrado')
        return render(request, 'novo_pet.html', context)


@login_required
def seus_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(usuario=request.user)

        context = {
            'pets' : pets
        }

        return render(request, 'seus_pets.html', context)


@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não é seu!')
        return redirect('/divulgar/seus_pets')

    pet.delete()
    messages.add_message(request, constants.SUCCESS, 'Removido com sucesso.')
    return redirect('/divulgar/seus_pets')


def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id = id)

        context = {
            'pet' : pet,
        }

        return render(request, 'ver_pet.html', context)


def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})


def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')


@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).filter(status="AP").count()# "__" para acessar outra coluna_
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]# lista so com os nomes
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)
