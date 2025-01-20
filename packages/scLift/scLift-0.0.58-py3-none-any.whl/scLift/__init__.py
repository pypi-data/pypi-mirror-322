# -*- coding: UTF-8 -*-

import os
import sys

from . import file as fl
from . import model as ml
from . import plot as pl
from . import preprocessing as pp
from . import tool as tl
from . import util as ul

from scLift.util import project_name, project_version

os.environ['OPENBLAS_NUM_THREADS'] = '1'
sys.setrecursionlimit(1000)

__version__ = f"{project_name}: v{project_version}"
__cache__ = ul.project_cache_path
