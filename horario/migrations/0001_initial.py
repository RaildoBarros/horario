# Generated by Django 2.2.2 on 2019-07-12 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sigla', models.CharField(max_length=10)),
                ('carga_horaria_semanal', models.PositiveIntegerField(verbose_name='Carga horária semanal (h)')),
                ('carga_horaria_semestral', models.PositiveIntegerField(verbose_name='Carga horária semestral (h)')),
                ('dificil', models.BooleanField(default=False, verbose_name='Difícil')),
                ('disciplina_estagio', models.BooleanField(default=False, verbose_name='Disciplina de Estágio')),
            ],
        ),
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('dia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoLetivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('inicio', models.DateField()),
                ('termino', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Períodos Letivos',
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('turno', models.CharField(choices=[('M', 'MATUTINO'), ('V', 'VESPERTINO'), ('N', 'NOTURNO')], max_length=2)),
                ('disciplinas', models.ManyToManyField(to='horario.Disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('carga_horaria_min_semanal', models.PositiveIntegerField(verbose_name='Carga horária mínima semanal (h)')),
                ('carga_horaria_max_semanal', models.PositiveIntegerField(verbose_name='Carga horária máxima semanal (h)')),
                ('disciplinas', models.ManyToManyField(blank=True, to='horario.Disciplina')),
            ],
            options={
                'verbose_name_plural': 'Professores',
            },
        ),
        migrations.CreateModel(
            name='Preferencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('SEG', 'SEGUNDA'), ('TER', 'TERÇA'), ('QUA', 'QUARTA'), ('QUI', 'QUINTA'), ('SEX', 'SEXTA'), ('SAB', 'SÁBADO')], max_length=3)),
                ('turno', models.CharField(choices=[('M', 'MATUTINO'), ('V', 'VESPERTINO'), ('N', 'NOTURNO')], max_length=2)),
                ('horario', models.CharField(choices=[('H1', 'H1'), ('H2', 'H2')], max_length=2)),
                ('professor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='horario.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='Lotacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horario.Disciplina')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horario.Professor')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horario.Turma')),
            ],
            options={
                'verbose_name_plural': 'Lotações',
            },
        ),
        migrations.CreateModel(
            name='Indisponibilidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('SEG', 'SEGUNDA'), ('TER', 'TERÇA'), ('QUA', 'QUARTA'), ('QUI', 'QUINTA'), ('SEX', 'SEXTA'), ('SAB', 'SÁBADO')], max_length=3)),
                ('turno', models.CharField(choices=[('M', 'MATUTINO'), ('V', 'VESPERTINO'), ('N', 'NOTURNO')], max_length=2)),
                ('horario', models.CharField(choices=[('H1', 'H1'), ('H2', 'H2')], max_length=2)),
                ('professor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='horario.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('carga_horaria', models.PositiveIntegerField(verbose_name='Carga horária (h)')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horario.Turma')),
            ],
        ),
    ]
