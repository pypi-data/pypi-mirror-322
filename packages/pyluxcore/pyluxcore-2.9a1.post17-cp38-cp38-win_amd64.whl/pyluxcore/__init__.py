# ****************************************************************************
# *                                                                          *
# * Copyright 2024 Howetuft <howetuft-at-gmail-dot-com>                      *
# *                                                                          *
# * Licensed under the Apache License, Version 2.0 (the "License");          *
# * you may not use this file except in compliance with the License.         *
# * You may obtain a copy of the License at                                  *
# *                                                                          *
# * http://www.apache.org/licenses/LICENSE-2.0                               *
# *                                                                          *
# * Unless required by applicable law or agreed to in writing, software      *
# * distributed under the License is distributed on an "AS IS" BASIS,        *
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
# * See the License for the specific language governing permissions and      *
# * limitations under the License.                                           *
# *                                                                          *
# ****************************************************************************


# start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyluxcore.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyluxcore-2.9a1.post17')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pyluxcore-2.9a1.post17')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

import platform
from pathlib import Path
import shutil

from .pyluxcore import *

_LUXFOLDER = Path(pyluxcore.__file__).parent

_OIDN_PATHS = {
    "Linux": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
    "Windows": (_LUXFOLDER / ".." / "pyluxcore.libs", "oidnDenoise.exe"),
    "Darwin": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
}

def which_oidn():
    """Retrieve external oidn path (applying which).

    Returns path only if oidn is there and executable, None otherwise.
    """
    path, executable = _OIDN_PATHS[platform.system()]
    denoiser_path = shutil.which(executable, path=path)
    return denoiser_path

def path_to_oidn():
    """Retrieve external oidn path.

    Just return theoretical path, do not check if oidn is there, nor if
    it is executable.
    """
    path, executable = _OIDN_PATHS[platform.system()]
    return path / executable
