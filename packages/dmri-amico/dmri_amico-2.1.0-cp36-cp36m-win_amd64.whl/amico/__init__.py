

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_4():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'dmri_amico.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-dmri_amico-2.1.0')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-dmri_amico-2.1.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_1_4()
del _delvewheel_init_patch_1_1_4
# end delvewheel patch

from amico.core import Evaluation, setup
from amico.util import set_verbose, get_verbose
# from amico import core
# from amico import scheme
# from amico import lut
# from amico import models
# from amico import util

__all__ = ['Evaluation', 'setup', 'set_verbose', 'get_verbose']

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version
__version__ = version('dmri-amico')
