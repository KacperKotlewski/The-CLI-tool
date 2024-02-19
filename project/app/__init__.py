from .root import app
import sys
import os

def run_cli() -> None:
    args = sys.argv[1:]
    app.execute(*args)