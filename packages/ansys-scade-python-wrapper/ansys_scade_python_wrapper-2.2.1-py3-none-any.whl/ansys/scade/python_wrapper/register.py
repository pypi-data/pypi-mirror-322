# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Registers the Code Generator extension registry files (SRG).

Refer to the :ref:`installation <getting_started/index:install in user mode>`
steps for more information.

It addresses SCADE 2024 R2 and prior releases.
SCADE 2025 R1 and above use the package's
``ansys.scade.registry`` entry point.
"""

import os
from pathlib import Path
import sys

_APPDATA = os.getenv('APPDATA')


def _register_srg_file(srg: Path, install: Path):
    # copy the srg file to Customize and patch it with the installation directory.
    text = srg.open().read()
    text = text.replace('%TARGETDIR%', install.as_posix())
    dst = Path(_APPDATA, 'SCADE', 'Customize', srg.name)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.open('w').write(text)


def _python_wrapper_config():
    # register the Code Generator extension registry files (SRG).
    script_dir = Path(__file__).parent
    # registrations depending on Python interpreter
    python_version = str(sys.version_info.major) + str(sys.version_info.minor)
    suffix = '23r1' if python_version == '37' else '24r2'
    _register_srg_file(script_dir / ('python_wrapper%s.srg' % suffix), script_dir)


def main():
    """Implement the ``ansys.scade.python_wrapper.register`` packages's project script."""
    _python_wrapper_config()


if __name__ == '__main__':
    main()
