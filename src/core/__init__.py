"""
Initialise the module.
Module path is included if not exists.
"""

import sys
import os

module_path = os.path.abspath(os.getcwd())
if module_path not in sys.path:
    sys.path.append(module_path)
