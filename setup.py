from cx_Freeze import setup, Executable

setup(
    name = "PROJECT_MICH",
    version = "0.1",
    author = "Grégory Mathez",
    author_email = "gregory.mathez@hotmail.ch",
    description = "Trading system for Poloniex",
    executables = [Executable("main.py")],
)