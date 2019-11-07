from django.contrib import admin

from .models import *

class TurmaAdmin(admin.ModelAdmin):
   list_display = ['id','nome', 'curso']
   search_fields = ['nome','curso']
   filter_horizontal = ('disciplinas',)

   list_per_page = 20

class LotacaoAdmin(admin.ModelAdmin):
   list_display = ['professor', 'turma', 'disciplina', 'curso']
   search_fields = ['professor__nome', 'turma__nome', 'disciplina__nome', 'turma__curso__nome']

   list_per_page = 20

class CursoAdmin(admin.ModelAdmin):
   list_display = ['id', 'nome']
   search_fields = ['nome']

   list_per_page = 20

class DisciplinaAdmin(admin.ModelAdmin):
   list_display = ['id', 'nome', 'carga_horaria_semanal', 'carga_horaria_semestral', 'dificil', 'disciplina_estagio']
   search_fields = ['nome']

   list_per_page = 20

class ProfessorAdmin(admin.ModelAdmin):
   list_display = ['nome', 'carga_horaria_min_semanal', 'carga_horaria_max_semanal', 'get_disciplinas']
   filter_horizontal = ('disciplinas',)
   search_fields = ['nome']

   list_per_page = 20

class PeriodoLetivoAdmin(admin.ModelAdmin):
   list_display = ['nome','inicio','termino']

   list_per_page = 20

class HorarioAdmin(admin.ModelAdmin):
   list_display = ['periodo_letivo','get_turmas','file']

   list_per_page = 20

admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Indisponibilidade)
admin.site.register(Lotacao, LotacaoAdmin)
admin.site.register(PeriodoLetivo, PeriodoLetivoAdmin)
admin.site.register(Feriado)
admin.site.register(Preferencia)
admin.site.register(Horario, HorarioAdmin)