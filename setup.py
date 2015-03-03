import sys
from distutils.core import setup

import py2exe

sys.path.append("..")
setup(name='rescache',
      version='0.1',
      description='Tool for managing the EVE shared cache',
      author='Snorri Sturluson',
      author_email='snorri.sturluson@ccpgames.com',
      options={
            "py2exe" : {
                  'bundle_files': 1,
                  'compressed': True,
            },
      },
      zipfile=None,
      console=['rescache.py'],
     )
