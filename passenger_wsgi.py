import os
import sys

INTERP = os.path.expanduser("/home/vpris/web/ctornton.ru/public_shtml/venv/bin/python3")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

