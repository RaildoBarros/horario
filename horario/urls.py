from django.urls import path

from . import views

app_name='horario'
urlpatterns = [
    path('', views.index, name='index'),
    path('gerarhorario', views.gerarhorario, name='gerarhorario'),
    path('horario/<int:pk>', views.horario, name='horario'),

    path('curso/list/', views.CursoListView.as_view(), name='cursos'),
    path('curso/add/', views.curso_add, name='curso_add'),
    path('curso/<int:pk>/edit/', views.curso_edit, name='curso_edit'),
    path('curso/<int:pk>/delete/', views.curso_delete, name='curso_delete'),

    path('disciplina/list/', views.DisciplinaListView.as_view(), name='disciplinas'),
    path('disciplina/add/', views.disciplina_add, name='disciplina_add'),
    path('disciplina/<int:pk>/edit/', views.disciplina_edit, name='disciplina_edit'),
    path('disciplina/<int:pk>/delete/', views.disciplina_delete, name='disciplina_delete'),

    path('feriado/list/', views.FeriadoListView.as_view(), name='feriados'),
    path('feriado/add/', views.feriado_add, name='feriado_add'),
    path('feriado/<int:pk>/edit/', views.feriado_edit, name='feriado_edit'),
    path('feriado/<int:pk>/delete/', views.feriado_delete, name='feriado_delete'),

    path('indisponibilidade/list/', views.IndisponibilidadListView.as_view(), name='indisponibilidades'),
    path('indisponibilidade/add/', views.indisponibilidade_add, name='indisponibilidade_add'),
    path('indisponibilidade/<int:pk>/edit/', views.indisponibilidade_edit, name='indisponibilidade_edit'),
    path('indisponibilidade/<int:pk>/delete/', views.indisponibilidade_delete, name='indisponibilidade_delete'),

    path('lotacao/list/', views.LotacaoListView.as_view(), name='lotacoes'),
    path('lotacao/add/', views.lotacao_add, name='lotacao_add'),
    path('lotacao/<int:pk>/edit/', views.lotacao_edit, name='lotacao_edit'),
    path('lotacao/<int:pk>/delete/', views.lotacao_delete, name='lotacao_delete'),

    path('periodoletivo/list/', views.PeriodoLetivoListView.as_view(), name='periodosletivos'),
    path('periodoletivo/add/', views.periodoletivo_add, name='periodoletivo_add'),
    path('periodoletivo/<int:pk>/edit/', views.periodoletivo_edit, name='periodoletivo_edit'),
    path('periodoletivo/<int:pk>/delete/', views.periodoletivo_delete, name='periodoletivo_delete'),

    path('preferencia/list/', views.PreferenciaListView.as_view(), name='preferencias'),
    path('preferencia/add/', views.preferencia_add, name='preferencia_add'),
    path('preferencia/<int:pk>/edit/', views.preferencia_edit, name='preferencia_edit'),
    path('preferencia/<int:pk>/delete/', views.preferencia_delete, name='preferencia_delete'),

    path('professor/list/', views.ProfessorListView.as_view(), name='professores'),
    path('professor/add/', views.professor_add, name='professor_add'),
    path('professor/<int:pk>/edit/', views.professor_edit, name='professor_edit'),
    path('professor/<int:pk>/delete/', views.professor_delete, name='professor_delete'),

    path('turma/list/', views.TurmaListView.as_view(), name='turmas'),
    path('turma/add/', views.turma_add, name='turma_add'),
    path('turma/<int:pk>/edit/', views.turma_edit, name='turma_edit'),
    path('turma/<int:pk>/delete/', views.turma_delete, name='turma_delete'),
]