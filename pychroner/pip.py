# coding=utf-8
import subprocess
import sys

class PIP:
    @classmethod
    def __init__(cls):
        if not cls.isInstalled():
            print("[Error] PIP is not installed in your system. Please install PIP first.")
            exit(1)

    @classmethod
    def isInstalled(cls):
        try:
            __import__("pip")
            return True
        except:
            return False

    @classmethod
    def installModule(cls, name: str):
        p = subprocess.run([sys.executable, "-m", "pip", "install", name])

        if p.returncode != 0:
            return False
        print(f"[PIP] installed {name}.")
        return True
