from django.db import models
from django.utils.safestring import mark_safe
from multiselectfield import MultiSelectField

DIAS_DA_SEMANA = (
        (u'SEG', u'SEGUNDA'),
        (u'TER', u'TERÇA'),
        (u'QUA', u'QUARTA'),
        (u'QUI', u'QUINTA'),
        (u'SEX', u'SEXTA'),
        (u'SAB', u'SÁBADO'),
)

TURNOS = (
        (u'M', u'MATUTINO'),
        (u'V', u'VESPERTINO'),
        (u'N', u'NOTURNO'),
)

INTERVALOS = (
        (u'H1', u'H1'),
        (u'H2', u'H2'),
)

class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10)
    carga_horaria_semanal = models.PositiveIntegerField(verbose_name='Carga horária semanal (h)')
    carga_horaria_semestral = models.PositiveIntegerField(verbose_name='Carga horária semestral (h)')
    dificil = models.BooleanField(default=False, verbose_name='Difícil')
    disciplina_estagio = models.BooleanField(default=False, verbose_name='Disciplina de Estágio')


    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    carga_horaria_min_semanal = models.PositiveIntegerField(verbose_name='Carga horária mínima semanal (h)')
    carga_horaria_max_semanal = models.PositiveIntegerField(verbose_name='Carga horária máxima semanal (h)')

    disciplinas = models.ManyToManyField(Disciplina, blank=True)

    def get_disciplinas(self):
        out = '<ul>'
        for d in self.disciplinas.all():
            out += '<li>' + str(d) + '</li>'
        out += '</ul>'
        return mark_safe(out)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Professores"

    get_disciplinas.short_description = 'Disciplinas'

class Indisponibilidade(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, unique=True)
    dia = models.CharField(max_length=3, choices=DIAS_DA_SEMANA)
    turno = models.CharField(max_length=2, choices=TURNOS)
    horario = models.CharField(max_length=2, choices=INTERVALOS)

    def __str__(self):
        return self.professor.nome

class Preferencia(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, unique=True)
    dia = models.CharField(max_length=3, choices=DIAS_DA_SEMANA)
    turno = models.CharField(max_length=2, choices=TURNOS)
    horario = models.CharField(max_length=2, choices=INTERVALOS)

    def __str__(self):
        return self.professor.nome

    class Meta:
        verbose_name_plural = "Preferências"
        verbose_name = "Preferência"

class Curso(models.Model):
    nome = models.CharField(max_length=200)
    carga_horaria = models.PositiveIntegerField(verbose_name='Carga horária (h)')

    def __str__(self):
        return self.nome

class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=True)
    nome = models.CharField(max_length=200)
    turno = models.CharField(max_length=2, choices=TURNOS)

    disciplinas = models.ManyToManyField(Disciplina)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.curso)

class Lotacao(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Lotações"

    def __str__(self):
        return self.turma.nome + " - " + self.disciplina.nome + " - " + self.professor.nome

    def curso(self):
        return self.turma.curso

class PeriodoLetivo(models.Model):
    nome = models.CharField(max_length=200)
    inicio = models.DateField(verbose_name='Início')
    termino = models.DateField(verbose_name='Término')

    class Meta:
        verbose_name_plural = "Períodos Letivos"

    def __str__(self):
        return self.nome

class Feriado(models.Model):
    nome = models.CharField(max_length=200)
    dia = models.DateField()

    def __str__(self):
        return self.nome

class Horario(models.Model):
    periodo_letivo = models.ForeignKey(PeriodoLetivo, verbose_name="Período Letivo", on_delete=models.CASCADE)
    turmas = models.ManyToManyField(Turma, verbose_name="Turmas")
    file = models.FileField(verbose_name="Horário")

    def get_turmas(self):
        out = '<ul>'
        for t in self.turmas.all():
            out += '<li>' + str(t) + '</li>'
        out += '</ul>'
        return mark_safe(out)

    class Meta:
        verbose_name_plural = "Horários"

    get_turmas.short_description = 'Turmas'

# poll = models.ForeignKey(Poll, verbose_name="the related poll")
# sites = models.ManyToManyField(Site, verbose_name="list of sites")
# place = models.OneToOneField(Place, verbose_name="related place")