from cx_Freeze import setup, Executable

setup(
    name="Escape from Zefira",
    version="1.0",
    description="Escape from Zefira",
    executables=[Executable("main.py")]
)