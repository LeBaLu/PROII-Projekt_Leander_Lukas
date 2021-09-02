#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
