from django.shortcuts import render, redirect
from divulgar.models import Pet, Raca
from django.contrib.messages import constants
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status="P")
        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            if raca_filter != "all":
                pets = pets.filter(raca__id=raca_filter)
                raca_filter = Raca.objects.get(id=raca_filter)

        context = {
            'pets' : pets,
            'racas' : racas,
            'cidade': cidade,
            'raca_filter': raca_filter,
        }

        return render(request, 'listar_pets.html', context)

@login_required
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.ERROR, 'Esse pet já foi adotado :)')
        return redirect('/adotar')

    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=request.user,
                          data=datetime.now())

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')

