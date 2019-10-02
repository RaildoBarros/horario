from django.contrib import admin

from .models import *

class TurmaAdmin(admin.ModelAdmin):
   list_display = ['id','nome', 'curso']
   search_fields = ['nome','curso']
   filter_horizontal = ('disciplinas',)

class LotacaoAdmin(admin.ModelAdmin):
   list_display = ['professor', 'turma', 'disciplina', 'curso']
   search_fields = ['professor__nome', 'turma__nome', 'disciplina__nome', 'turma__curso__nome']

class CursoAdmin(admin.ModelAdmin):
   list_display = ['id', 'nome']
   search_fields = ['nome']

class DisciplinaAdmin(admin.ModelAdmin):
   list_display = ['id', 'nome', 'carga_horaria_semanal', 'carga_horaria_semestral', 'dificil', 'disciplina_estagio']
   search_fields = ['nome']

class ProfessorAdmin(admin.ModelAdmin):
   filter_horizontal = ('disciplinas',)
   search_fields = ['nome']
   filter_horizontal = ('disciplinas',)

admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Indisponibilidade)
admin.site.register(Lotacao, LotacaoAdmin)
admin.site.register(PeriodoLetivo)
admin.site.register(Feriado)
admin.site.register(Preferencia)