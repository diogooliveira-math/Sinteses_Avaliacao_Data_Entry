#!/usr/bin/env python3
"""Legacy wrapper: `check_db.py` moved to `scripts/check_db.py`.

This small wrapper maintains backward compatibility when invoked
from the project root.
"""
import runpy
import os

script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'check_db.py')
if os.path.exists(script_path):
    runpy.run_path(script_path, run_name='__main__')
else:
    print("Moved: scripts/check_db.py not found. See docs/ for organization.")
