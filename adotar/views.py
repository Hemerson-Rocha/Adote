from django.shortcuts import render
from divulgar.models import Pet, Raca

def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status="P")
        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            if raca_filter == "all":
                pets = pets.all()
            else:
                pets = pets.filter(raca__id=raca_filter)
                raca_filter = Raca.objects.get(id=raca_filter)

        context = {
            'pets' : pets,
            'racas' : racas,
            'cidade': cidade,
            'raca_filter': raca_filter,
        }

        return render(request, 'listar_pets.html', context)