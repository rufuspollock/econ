#!/usr/bin/env python

from distutils.core import setup

import sys
sys.path.append('./src')
from econ import __version__

setup(name="OKF Economics",
      version=__version__,
      description="OKF Economics Package",
      license = 'GPL',
      author="Rufus Pollock and Others (see AUTHORS)",
      url="http://project.knowledgeforge.net/econ/",
      package_dir = { '' : 'src' },
      packages=['econ']
     )
