from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import *

class CursoForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = ('nome','carga_horaria')

class DisciplinaForm(forms.ModelForm):

    class Meta:
        model = Disciplina
        fields = ('nome','sigla', 'carga_horaria_semanal', 'carga_horaria_semestral', 'dificil', 'disciplina_estagio')

class FeriadoForm(forms.ModelForm):

    class Meta:
        model = Feriado
        fields = ('nome','dia')

class IndisponibilidadeForm(forms.ModelForm):

    class Meta:
        model = Indisponibilidade
        fields = ('professor','dia','turno','horario')

class LotacaoForm(forms.ModelForm):

    class Meta:
        model = Lotacao
        fields = ('professor','turma','disciplina')

class PeriodoLetivoForm(forms.ModelForm):

    class Meta:
        model = PeriodoLetivo
        fields = ('nome','inicio','termino')

class PreferenciaForm(forms.ModelForm):

    class Meta:
        model = Preferencia
        fields = ('professor','dia','turno','horario')

class ProfessorForm(forms.ModelForm):

    class Meta:
        model = Professor
        fields = ('nome','carga_horaria_min_semanal','carga_horaria_max_semanal','disciplinas')

class TurmaForm(forms.ModelForm):

    class Meta:
        model = Turma
        fields = ('curso','nome','turno','disciplinas')

class GerarHorarioForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())

