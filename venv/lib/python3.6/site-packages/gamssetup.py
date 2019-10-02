#!/usr/bin/env python

from distutils.core import setup
import os

def run_setup():

    libs = ["workspace", "database", "execution", "options"]

    suffix = ""
    if os.name == "posix":
        suffix = ".so"
    elif os.name == "nt":
        suffix = ".pyd"
    else:
        raise Exception("could not determine operating system")

    libs = [l + suffix for l in libs]

    setup(name='GAMS',
          version='1.0',
          description='GAMS API',
          author='GAMS',
          packages=["gams"],
          package_data={"gams": libs}
    )

    
if __name__ == "__main__":
    run_setup()