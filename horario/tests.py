import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gradehoraria.settings'
import django
django.setup()

from horario.models import *
from horario import horario_bridge

curso = Curso.objects.get(pk=7)
turmas = Turma.objects.filter(curso=curso)

def teste_send_to_neos_server():
    horario_bridge.obter_dados_gdx(curso.pk)
    horario_bridge.gdx_to_base64('./files/in.gdx')
    horario_bridge.send_to_neos_server()

def teste_obter_arquivo():
    import argparse
    import zipfile
    try:
        import xmlrpc.client as xmlrpclib
    except ImportError:
        import xmlrpclib

    print('Testando a obtenção do arquivo...')
    args = argparse.Namespace(action='./files/job.xml', password=None, server='https://neos-server.org:3333', username=None)
    neos = xmlrpclib.ServerProxy(args.server)

    jobNumber = 7572546
    password = 'sQCYnWaK'
    fileName = 'solver-output.zip'

    output_file = neos.getOutputFile(jobNumber, password, fileName)
    out_zip = open('./files/out.zip', 'wb')
    out_zip.write(output_file.data)
    zip = zipfile.ZipFile('./files/out.zip')
    zip.extractall('./files')
    zip.close()

def ler_resultado():

    from gams import GamsWorkspace

    ws = GamsWorkspace(working_directory="./files")

    # add a new GamsDatabase and initialize it from the GDX file just created
    db2 = ws.add_database_from_gdx("out.gdx")

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

def teste_gams_linux():
    from gams import GamsWorkspace
    import platform
    from gradehoraria import settings
    working_directory = settings.BASE_DIR

    if platform.system() == 'Linux':
        GAMS_PATH = '/opt/gams28.2'
    else:
        GAMS_PATH = 'c:/GAMS'

    ws = GamsWorkspace(system_directory=GAMS_PATH, working_directory=working_directory)


########### ÁREA DE TESTES ###########

# print(horario_bridge.ler_resultado(turmas))
# print(horario_bridge.obter_dados_gdx(7))
# print(horario_bridge.gerar_horario(7))
