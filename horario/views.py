from datetime import timedelta
import time

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from . import horario_bridge
from .forms import *
from .models import *
import math
from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
            pass
mysite = MyAdminSite()

@login_required(redirect_field_name='next', login_url='/horario')
def index(request):
    username = request.user
    total_cursos = Curso.objects.all().count()
    total_disciplinas = Disciplina.objects.all().count();
    total_professores = Professor.objects.all().count()
    total_turmas = Turma.objects.all().count()
    total_indisponibilidades = Indisponibilidade.objects.all().count()
    total_preferencias = Preferencia.objects.all().count()
    template_name = 'horario/index.html'
    context = {
        'total_disciplinas': total_disciplinas,
        'total_cursos': total_cursos,
        'total_professores': total_professores,
        'total_turmas': total_turmas,
        'total_indisponibilidades': total_indisponibilidades,
        'total_preferencias': total_preferencias,
        'has_permission': mysite.has_permission(request),
        'username': username,
    }
    return render(request, template_name, context)

@login_required()
def gerarhorario(request):
    form = GerarHorarioForm()
    template_name = 'horario/gerarhorario.html'

    if request.method == "POST":
        form = GerarHorarioForm(request.POST)
        if form.is_valid():
            turmas = form.cleaned_data['turmas']
            periodo_letivo = form.cleaned_data['periodo_letivo']
            horario_id = horario_bridge.gerar_horario(turmas, periodo_letivo)
            if horario_id:
                messages.success(request, "Horário Gerado com sucesso!")
                return redirect('horario:horario', pk=horario_id)
            else:
                messages.error(request, "Não foi possível gerar o horário!")

    else:
        form = GerarHorarioForm()
    context = {
        'form': form,
        'has_permission': mysite.has_permission(request),
    }
    return render(request, template_name, context)

class HorarioListView(ListView):
    model = Horario

def obter_semanas(periodo_letivo):
    semanas = []
    qtd_semanas = math.ceil((periodo_letivo.termino - periodo_letivo.inicio).days / 7)
    for i in range(qtd_semanas):
        semanas.append((i,'s'+str(i+1)))
    return semanas

def obter_segunda(periodo_letivo):
    data = periodo_letivo.inicio
    while data.weekday() != 0:
        data = data - timedelta(days=1)
    return data

@login_required()
def horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    semanas = obter_semanas(horario.periodo_letivo)
    dias_feriados = Feriado.objects.values_list('dia', flat=True)
    resultado = horario_bridge.ler_resultado(horario.turmas.all(), horario.file.path)
    template_name = 'horario/horario.html'
    context = {
        'resultado': resultado,
        'turmas': horario.turmas.all(),
        'dias_da_semana': DIAS_DA_SEMANA,
        'primeiro_dia': obter_segunda(horario.periodo_letivo),
        'semanas': semanas,
        'periodo_letivo': horario.periodo_letivo,
        'dias_feriados': dias_feriados,
        'has_permission': mysite.has_permission(request)
    }

    return render(request, template_name, context)