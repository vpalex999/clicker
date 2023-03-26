import os
import platform
import PyInstaller.__main__

def make_build():
    machine = platform.machine()

    name = f"clicker-{platform.system()}-{machine}"
    PyInstaller.__main__.run([
        f"--name={name}",
        "--onefile",
        "--clean",
        "--workpath=installer/build",
        "--distpath=./",
        "--specpath=installer",
        os.path.join('.', "clicker.py")
    ])


if __name__ == "__main__":
    make_build()