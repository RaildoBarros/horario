from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from . import horario_bridge
from .forms import *
from .models import *
import math

template_edit = 'horario/edit.html'

def index(request):
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
    }
    return render(request, template_name, context)

def gerarhorario(request):
    form = GerarHorarioForm()
    template_name = 'horario/gerarhorario.html'
    if request.method == "POST":
        form = GerarHorarioForm(request.POST)
        if form.is_valid():
            curso_id = request.POST.dict().get('curso')
            return redirect('horario:horario', pk=curso_id)
    else:
        form = GerarHorarioForm()
    return render(request, template_name, {'form': form})

def obter_semanas():
    semanas = []
    periodo_letivo = PeriodoLetivo.objects.get(id=1)
    qtd_semanas = math.ceil((periodo_letivo.termino - periodo_letivo.inicio).days / 7)
    for i in range(qtd_semanas):
        semanas.append('s'+str(i+1))
    return semanas

def horario(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    turmas = Turma.objects.filter(curso=curso)
    semanas = obter_semanas()
    resultados = horario_bridge.gerar_horario(pk)
    template_name = 'horario/horario.html'
    context = {
        'resultados': resultados,
        'turmas': turmas,
        'dias_da_semana': DIAS_DA_SEMANA,
        'semanas': semanas,
    }

    return render(request, template_name, context)

#######################################################
class CursoListView(ListView):
    model = Curso

def curso_add(request):
    form = CursoForm()
    template_name = template_edit
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso adicionado com sucesso')
            return redirect('horario:cursos')
    else:
        form = CursoForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso salvo com sucesso')
            return redirect('horario:cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'O curso foi excluído com sucesso')
        return redirect('horario:cursos')
    template = 'horario/curso_delete.html'
    context = {
        'curso': curso,
    }
    return render(request, template, context)

#######################################################
class DisciplinaListView(ListView):
    model = Disciplina

def disciplina_add(request):
    form = DisciplinaForm()
    template_name = template_edit
    if request.method == "POST":
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina adicionada com sucesso')
            return redirect('horario:disciplinas')
    else:
        form = DisciplinaForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def disciplina_edit(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina salva com sucesso')
            return redirect('horario:disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def disciplina_delete(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        disciplina.delete()
        messages.success(request, 'A disciplina foi excluída com sucesso')
        return redirect('horario:disciplinas')
    template = 'horario/disciplina_delete.html'
    context = {
        'disciplina': disciplina,
    }
    return render(request, template, context)

#######################################################
class FeriadoListView(ListView):
    model = Feriado

def feriado_add(request):
    form = FeriadoForm()
    template_name = template_edit
    if request.method == "POST":
        form = FeriadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feriado adicionado com sucesso')
            return redirect('horario:feriados')
    else:
        form = FeriadoForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def feriado_edit(request, pk):
    feriado = get_object_or_404(Feriado, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = FeriadoForm(request.POST, instance=feriado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feriado salvo com sucesso')
            return redirect('horario:feriados')
    else:
        form = FeriadoForm(instance=feriado)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def feriado_delete(request, pk):
    feriado = get_object_or_404(Feriado, pk=pk)
    if request.method == 'POST':
        feriado.delete()
        messages.success(request, 'O feriado foi excluído com sucesso')
        return redirect('horario:feriados')
    template = 'horario/feriado_delete.html'
    context = {
        'feriado': feriado,
    }
    return render(request, template, context)
#######################################################
class IndisponibilidadListView(ListView):
    model = Indisponibilidade

def indisponibilidade_add(request):
    form = IndisponibilidadeForm()
    template_name = template_edit
    if request.method == "POST":
        form = IndisponibilidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Indisponibilidade adicionada com sucesso')
            return redirect('horario:indisponibilidades')
    else:
        form = IndisponibilidadeForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def indisponibilidade_edit(request, pk):
    indisponibilidade = get_object_or_404(Indisponibilidade, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = IndisponibilidadeForm(request.POST, instance=indisponibilidade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Indisponibilidade salva com sucesso')
            return redirect('horario:indisponibilidades')
    else:
        form = IndisponibilidadeForm(instance=indisponibilidade)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def indisponibilidade_delete(request, pk):
    indisponibilidade = get_object_or_404(Indisponibilidade, pk=pk)
    if request.method == 'POST':
        indisponibilidade.delete()
        messages.success(request, 'A indisponibilidade foi excluída com sucesso')
        return redirect('horario:indisponibilidades')
    template = 'horario/indisponibilidade_delete.html'
    context = {
        'indisponibilidade': indisponibilidade,
    }
    return render(request, template, context)
#######################################################
class LotacaoListView(ListView):
    model = Lotacao

def lotacao_add(request):
    form = LotacaoForm()
    template_name = template_edit
    if request.method == "POST":
        form = LotacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lotação adicionada com sucesso')
            return redirect('horario:lotacoes')
    else:
        form = LotacaoForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def lotacao_edit(request, pk):
    lotacao = get_object_or_404(Lotacao, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = LotacaoForm(request.POST, instance=lotacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lotação salva com sucesso')
            return redirect('horario:lotacoes')
    else:
        form = LotacaoForm(instance=lotacao)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def lotacao_delete(request, pk):
    lotacao = get_object_or_404(Lotacao, pk=pk)
    if request.method == 'POST':
        lotacao.delete()
        messages.success(request, 'A lotação foi excluída com sucesso')
        return redirect('horario:lotacoes')
    template = 'horario/lotacao_delete.html'
    context = {
        'lotacao': lotacao,
    }
    return render(request, template, context)
#######################################################
class PeriodoLetivoListView(ListView):
    model = PeriodoLetivo

def periodoletivo_add(request):
    form = PeriodoLetivoForm()
    template_name = template_edit
    if request.method == "POST":
        form = PeriodoLetivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodo Letivo adicionado com sucesso')
            return redirect('horario:periodosletivos')
    else:
        form = PeriodoLetivoForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def periodoletivo_edit(request, pk):
    periodoletivo = get_object_or_404(PeriodoLetivo, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = PeriodoLetivoForm(request.POST, instance=periodoletivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Períodos Letivos salva com sucesso')
            return redirect('horario:periodosletivos')
    else:
        form = PeriodoLetivoForm(instance=periodoletivo)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def periodoletivo_delete(request, pk):
    periodoletivo = get_object_or_404(PeriodoLetivo, pk=pk)
    if request.method == 'POST':
        periodoletivo.delete()
        messages.success(request, 'O período letivo foi excluído com sucesso')
        return redirect('horario:periodosletivos')
    template = 'horario/periodoletivo_delete.html'
    context = {
        'periodoletivo': periodoletivo,
    }
    return render(request, template, context)
#######################################################
class PreferenciaListView(ListView):
    model = Preferencia

def preferencia_add(request):
    form = PreferenciaForm()
    template_name = template_edit
    if request.method == "POST":
        form = PreferenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferência adicionada com sucesso')
            return redirect('horario:preferencias')
    else:
        form = PreferenciaForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def preferencia_edit(request, pk):
    preferencia = get_object_or_404(Preferencia, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = PreferenciaForm(request.POST, instance=preferencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferência salva com sucesso')
            return redirect('horario:preferencias')
    else:
        form = PreferenciaForm(instance=preferencia)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def preferencia_delete(request, pk):
    preferencia = get_object_or_404(Preferencia, pk=pk)
    if request.method == 'POST':
        preferencia.delete()
        messages.success(request, 'A preferência foi excluído com sucesso')
        return redirect('horario:preferencias')
    template = 'horario/preferencia_delete.html'
    context = {
        'preferencia': preferencia,
    }
    return render(request, template, context)
#######################################################
class ProfessorListView(ListView):
    model = Professor

def professor_add(request):
    form = ProfessorForm()
    template_name = template_edit
    if request.method == "POST":
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor adicionado com sucesso')
            return redirect('horario:professores')
    else:
        form = ProfessorForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def professor_edit(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor salvo com sucesso')
            return redirect('horario:professores')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        professor.delete()
        messages.success(request, 'O professor foi excluído com sucesso')
        return redirect('horario:professores')
    template = 'horario/professor_delete.html'
    context = {
        'professor': professor,
    }
    return render(request, template, context)
#######################################################
class TurmaListView(ListView):
    model = Turma

def turma_add(request):
    form = TurmaForm()
    template_name = template_edit
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma adicionada com sucesso')
            return redirect('horario:turmas')
    else:
        form = TurmaForm()
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def turma_edit(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    template_name = template_edit
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma salva com sucesso')
            return redirect('horario:turmas')
    else:
        form = TurmaForm(instance=turma)
    return render(request, template_name, {'form': form, 'nome': form.Meta.model.__name__})

def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'A turma foi excluída com sucesso')
        return redirect('horario:turmas')
    template = 'horario/turma_delete.html'
    context = {
        'turma': turma,
    }
    return render(request, template, context)
