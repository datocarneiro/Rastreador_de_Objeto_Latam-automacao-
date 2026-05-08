import sys
from cx_Freeze import setup, Executable

# Adiciona automaticamente o argumento "build" caso não seja fornecido
if "build" not in sys.argv:
    sys.argv.append("build")

# Definir as opções de build
build_exe_options = {
    "packages": ["os", "flask", "pandas", "selenium", "webdriver_manager", "openpyxl"],
    "include_files": [".env"],
    "include_msvcr": True,  # Inclui as DLLs do Visual C++
}

# Base para a criação do executável
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Remove a janela do console se estiver usando interface gráfica

# Configuração do cx_Freeze
setup(
    name="Dato_Latam.v2",
    version="2.0",
    description="Aplicação gera e rastreia encomendas Latam!",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="static/icone.ico")],
)
