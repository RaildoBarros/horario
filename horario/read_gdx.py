import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'gradehoraria.settings'
import django
django.setup()

from gams import *

from horario import Lotacao

def lerResultado():
    ws = GamsWorkspace(working_directory="./files")

    # add a new GamsDatabase and initialize it from the GDX file just created
    db2 = ws.add_database_from_gdx("out.gdx")

    x = dict((tuple(rec.keys), rec.level) for rec in db2["x"])
    alocacao = []
    for r in x:
        if x[r] == 1:
            alocacao.append(r)

    lotacao = Lotacao.objects.all()

    resultado = []
    for a in alocacao:
        for l in lotacao:
            if int(a[0]) == l.disciplina.pk:
                resultado.append([l,a[1],a[4],a[2],a[3]])

    return resultado;



print(lerResultado())
