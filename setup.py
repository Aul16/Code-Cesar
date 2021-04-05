import sys
from cx_Freeze import setup, Executable

include_files = ["dico.txt", "logo.ico"]
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="CodeCesar",
      version="0.1",
      description="Chiffrage / Déchiffrage auto de code césar",
      options={"build_exe": {"include_files": include_files}},
      executables=[Executable("app.py", base=base)])
