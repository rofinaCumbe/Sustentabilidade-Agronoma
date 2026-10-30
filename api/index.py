"""
Ponto de entrada do Vercel Serverless Function (api/index.py).
Reexporta a aplicação ASGI app.py para total compatibilidade com Vercel.
"""

import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, application, handler

__all__ = ["app", "application", "handler"]
