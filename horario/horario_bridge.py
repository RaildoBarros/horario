from __future__ import print_function

import os
import math
from builtins import print
from unicodedata import normalize
from datetime import timedelta
from .models import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'gradehoraria.settings'
import django
django.setup()

from gams import GamsWorkspace
import platform
from gradehoraria import settings
working_directory = settings.BASE_DIR

if platform.system() == 'Linux':
    GAMS_PATH = '/opt/gams28.2'
elif platform.system() == 'Windows':
    GAMS_PATH = 'C:/GAMS/win64/27.2'

ws = GamsWorkspace(system_directory=GAMS_PATH, working_directory=working_directory)


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

# Recebe o id do curso
def obter_dados_gdx(curso_id):

    # if len(sys.argv) > 1:
    #     ws = GamsWorkspace(system_directory=sys.argv[1])
    # else:
    #     ws = GamsWorkspace(working_directory="./gams_files")

    # ws = GamsWorkspace(working_directory="./files")

    # Pega os dados das tabelas
    curso = Curso.objects.get(id=curso_id)
    turmas_query = Turma.objects.filter(curso=curso)
    ids_disciplinas = Lotacao.objects.values_list('disciplina', flat=True).filter(turma__in=turmas_query)
    disciplinas_query = Disciplina.objects.filter(pk__in=set(ids_disciplinas))
    ids_professores = Lotacao.objects.values_list('professor', flat=True).filter(turma__in=turmas_query)
    professores_query = Professor.objects.filter(pk__in=set(ids_professores))
    periodo_letivo = PeriodoLetivo.objects.get(id=1)
    feriados_query = Feriado.objects.all()
    disponibilidades_query = Indisponibilidade.objects.filter(professor__in=professores_query)
    preferencias_query = Preferencia.objects.filter(professor__in=professores_query)

    # Inicializa os arrays e objetos
    disciplinas = []
    professores = []
    turmas = []
    turnos = []
    semanas = []
    horarios = []
    dias = []
    cmin_param = {}
    cmax_param = {}
    ch_param = {}
    chs_param = {}
    dg_param = {}
    dp_param = {}
    gt_param = {}
    feriados = {}
    disciplinas_dificeis = {}
    disciplinas_estagio = {}
    disponibilidades = {}
    preferencias = {}

    # Pega os dados separando as colunas para um array ou objeto
    for d in disciplinas_query:
        disciplinas.append(d.nome)
        ch_param[d.nome] = d.carga_horaria_semanal/2
        chs_param[d.nome] = d.carga_horaria_semestral/2

        # Popula disciplinas_dificeis
        if d.dificil:
            disciplinas_dificeis[d.nome] = 1
        else:
            disciplinas_dificeis[d.nome] = 0

        # Popula disciplinas_estagio
        if d.disciplina_estagio:
            disciplinas_estagio[d.nome] = 1
        else:
            disciplinas_estagio[d.nome] = 0

        for t in turmas_query:
            # Popula dg
            aux = False
            for dd in t.disciplinas.all():
                if dd.id == d.id:
                    aux = True
            if aux:
                dg_param[d.nome, t.nome] = 1
            else:
                dg_param[d.nome, t.nome] = 0

            # Popula gt
            for turno in TURNOS:
                if t.turno == turno[0]:
                    gt_param[t.nome, turno[0]] = 1
                else:
                    gt_param[t.nome, turno[0]] = 0

        for p in professores_query:
            aux = False
            for dd in p.disciplinas.all():
                if dd.id == d.id:
                    aux = True
            if aux:
                dp_param[d.nome, p.nome] = 1
            else:
                dp_param[d.nome, p.nome] = 0

    for p in professores_query:
        professores.append(p.nome)
        cmin_param[p.nome] = p.carga_horaria_min_semanal / 2
        cmax_param[p.nome] = p.carga_horaria_max_semanal / 2

    for t in turmas_query:
        turmas.append(t.nome)

    for t in TURNOS:
        turnos.append(t[0])

    # Preenche o array dias
    for j in DIAS_DA_SEMANA:
        dias.append(j[0])

    # Preenche o array horarios
    for h in INTERVALOS:
        horarios.append(h[0])

    # Contabilizar quantas semanas tem o período letivo e preenche os dados da semana
    qtd_semanas = math.ceil((periodo_letivo.termino - periodo_letivo.inicio).days / 7)
    for i in range(qtd_semanas):
        semanas.append('s'+str(i+1))

    # Preenche os dados de dias feriados
    for s in semanas:
        for j in dias:
            feriados[s,j] = 1

    dias_antes = periodo_letivo.inicio.weekday()
    for p in reversed(range(dias_antes)):
        feriados[semanas[0],dias[p]] = 0

    dias_depois = (len(dias)-1) - periodo_letivo.termino.weekday()
    for p in range(dias_depois):
        feriados[semanas[-1], dias[p]] = 0

    dia = periodo_letivo.inicio
    for p in range((periodo_letivo.termino - periodo_letivo.inicio).days+1):
        for f in feriados_query:
            if(dia == f.dia):
                feriados[semanas[p//7], dias[dia.weekday()]] = 0
        dia = periodo_letivo.inicio + timedelta(days=p+1)

    # Preenche as disponibilidades
    for p in professores_query:
        for j in dias:
            for t in turnos:
                if (j == 'SAB' and t == 'V'):
                    break
                for h in horarios:
                    disponibilidades[p.nome, j, t, h] = 1

    for d in disponibilidades_query:
        disponibilidades[d.professor.nome, d.dia, d.turno, d.horario] = 0

    # Preenche as preferencias
    for p in professores_query:
        for j in dias:
            for t in turnos:
                if (j == 'SAB' and t == 'V'):
                    break
                for h in horarios:
                    preferencias[p.nome, j, t, h] = 0

    for p in preferencias_query:
        preferencias[p.professor.nome, p.dia, p.turno, p.horario] = 1

    # Adiciona os dados ao banco de dados GAMS
    db = ws.add_database()

    d = db.add_set("d", 1, "disciplinas")
    for disc in disciplinas:
        d.add_record(disc)

    p = db.add_set("p", 1, "professores")
    for pp in professores:
        p.add_record(pp)

    g = db.add_set("g", 1, "turmas")
    for gg in turmas:
        g.add_record(gg)

    t = db.add_set("t", 1, "turnos")
    for tt in turnos:
        t.add_record(tt)

    s = db.add_set("s", 1, "semanas")
    for ss in semanas:
        s.add_record(ss)

    h = db.add_set("h", 1, "horarios")
    for hh in horarios:
        h.add_record(hh)

    j = db.add_set("j", 1, "dias")
    for jj in dias:
        j.add_record(jj)

    ch = db.add_parameter_dc("ch", [d], "carga horaria semanal da disciplina")
    for disc in disciplinas:
        ch.add_record(disc).value = ch_param[disc]

    chs = db.add_parameter_dc("chs", [d], "carga horaria semestral da disciplina")
    for disc in disciplinas:
        chs.add_record(disc).value = chs_param[disc]

    cmin = db.add_parameter_dc("cmin", [p], "carga horaria minima semanal do professor")
    for pp in professores:
        cmin.add_record(pp).value = cmin_param[pp]

    cmax = db.add_parameter_dc("cmax", [p], "carga horaria maxima semanal do professor")
    for pp in professores:
        cmax.add_record(pp).value = cmax_param[pp]

    dd = db.add_parameter_dc("dd", [d], "disciplinas consideradas difíceis")
    for disc in disciplinas:
        dd.add_record(disc).value = disciplinas_dificeis[disc]

    de = db.add_parameter_dc("de", [d], "disciplinas de estágio")
    for disc in disciplinas:
        de.add_record(disc).value = disciplinas_estagio[disc]

    dg = db.add_parameter_dc("dg", [d, g], "disciplinas pertencentes as turmas")
    for k, v in iter(dg_param.items()):
        dg.add_record(k).value = v

    dp = db.add_parameter_dc("dp", [d, p], "disciplinas pertencentes aos professores")
    for k, v in iter(dp_param.items()):
        dp.add_record(k).value = v

    gt = db.add_parameter_dc("gt", [g, t], "turnos das disciplinas")
    for k, v in iter(gt_param.items()):
        gt.add_record(k).value = v

    f = db.add_parameter_dc("f", [s, j], "feriados")
    for k, v in iter(feriados.items()):
        f.add_record(k).value = v

    disp = db.add_parameter_dc("disp", [p, j, t, h], "disponibilidades dos professores")
    for k, v in iter(disponibilidades.items()):
        disp.add_record(k).value = v

    pref = db.add_parameter_dc("pref", [p, j, t, h], "preferencias dos professores")
    for k, v in iter(preferencias.items()):
        pref.add_record(k).value = v

    nome_curso = remover_acentos(curso.nome.lower().replace(" ","_"))
    db.export('horario/files/in.gdx')

def send_to_neos_server():
    import argparse
    import sys
    import time
    import zipfile

    try:
        import xmlrpc.client as xmlrpclib
    except ImportError:
        import xmlrpclib

    print("Enviando para neos server...")
    args = argparse.Namespace(action='files/job.xml', password=None, server='https://neos-server.org:3333', username=None)

    neos = xmlrpclib.ServerProxy(args.server)

    alive = neos.ping()
    if alive != "NeosServer is alive\n":
        sys.stderr.write("Could not make connection to NEOS Server\n")
        sys.exit(1)
    if args.action == "queue":
        msg = neos.printQueue()
        sys.stdout.write(msg)
    else:
        xml = ""
        try:
            xmlfile = open(args.action, "r")
            buffer = 1
            while buffer:
                buffer = xmlfile.read()
                xml += buffer
            xmlfile.close()
        except IOError as e:
            sys.stderr.write("I/O error(%d): %s\n" % (e.errno, e.strerror))
            sys.exit(1)
        if args.username and args.password:
            (jobNumber, password) = neos.authenticatedSubmitJob(xml, args.username, args.password)
        else:
            (jobNumber, password) = neos.submitJob(xml)
        sys.stdout.write("Job number = %d\nJob password = %s\n" % (jobNumber, password))
        if jobNumber == 0:
            sys.stderr.write("NEOS Server error: %s\n" % password)
            sys.exit(1)
        else:
            offset = 0
            status = ""
            while status != "Done":
                time.sleep(1)
                (msg, offset) = neos.getIntermediateResults(jobNumber, password, offset)
                sys.stdout.write(msg.data.decode())
                status = neos.getJobStatus(jobNumber, password)
            msg = neos.getFinalResults(jobNumber, password)
            sys.stdout.write(msg.data.decode())

            print('Obtendo arquivo solução...')
            fileName = 'solver-output.zip'
            output_file = neos.getOutputFile(jobNumber, password, fileName)
            out_zip = open('./files/out.zip', 'wb')
            out_zip.write(output_file.data)

            zip = zipfile.ZipFile('./files/out.zip')
            zip.extractall('./files')
            zip.close()

def gdx_to_base64(file):
    import base64

    xml = 'files/job.xml'

    with open(file, 'rb') as file:
        data = base64.b64encode(file.read())

    string_base64 = str(data)
    string_base64 = (string_base64 + 'b').strip("'b")
    file.close()

    lines = open(xml).readlines()
    lines[117] = string_base64 + '\n'
    open(xml, 'w').writelines(lines)

def ler_resultado(turmas):
    # add a new GamsDatabase and initialize it from the GDX file just created
    db2 = ws.add_database_from_gdx("horario/files/out.gdx")
    x = dict((tuple(rec.keys), rec.level) for rec in db2["x"])
    alocacao = []
    for r in x:
        if x[r] == 1:
            alocacao.append(r)

    lotacao = Lotacao.objects.filter(turma__in=turmas)
    resultado = []
    for a in alocacao:
        for l in lotacao:
            # if int(a[0]) == l.disciplina.pk:
            # a[0] -> disciplina
            # a[1] -> semana
            # a[2] -> turno
            # a[3] -> horario
            # a[4] -> dia da semana
            if a[0] == l.disciplina.nome:
                resultado.append([l, a[1], a[4], a[2], a[3]])

    return resultado;

def gerar_horario(curso_id):
    curso = Curso.objects.get(pk=curso_id)
    turmas = Turma.objects.filter(curso=curso)

    obter_dados_gdx(curso_id)
    gdx_to_base64('files/in.gdx')
    send_to_neos_server()
    resultado = ler_resultado(turmas)

    return resultado
