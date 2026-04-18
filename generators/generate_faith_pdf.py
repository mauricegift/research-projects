#!/usr/bin/env python3
"""PDF wrapper for Faith Awuor Okumu's research project."""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

from generate_faith_docx import generate, convert_to_pdf

if __name__ == '__main__':
    generate()
    convert_to_pdf()
