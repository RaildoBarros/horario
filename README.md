- Instalar GAMS Release 27.2.0
- Instalar python3.6
- Na pasta C:\GAMS\win64\27.2\apifiles\Python\api36, executar:
python setup.py install
- Copiar modelo .gms e dados.xls para C:\GAMS\win64\27.2\datalib_ml

-Imports:
    
    from __future__ import print_function
    
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'gradehoraria.settings'
    import django
    django.setup()
    
    from gams import *
    import sys
    from horario.models import *