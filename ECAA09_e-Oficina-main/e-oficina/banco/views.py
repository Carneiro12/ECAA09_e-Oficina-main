from django.shortcuts import render
from banco.models import Servico

def servico_index(request):
    servicos = Servico.objects.all()
    context = {"servicos": servicos}
    return render(request, "servico_index.html", context)

def servico_detail(request, servico_id):
    servico = Servico.objects.get(id=servico_id)
    context = {"servico": servico}
    return render(request, "servico_detail.html", context)