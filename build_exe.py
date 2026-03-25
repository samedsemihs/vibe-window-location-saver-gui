"""Build script to create a standalone .exe using PyInstaller."""
import PyInstaller.__main__
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(script_dir, "main.py"),
    "--name=ScreenLocSaver",
    "--onefile",
    "--windowed",              # No console window
    "--noconfirm",
    f"--distpath={os.path.join(script_dir, 'dist')}",
    f"--workpath={os.path.join(script_dir, 'build')}",
    f"--specpath={script_dir}",
    # Include all modules
    "--hidden-import=pystray._win32",
    "--hidden-import=PIL._tkinter_finder",
])
