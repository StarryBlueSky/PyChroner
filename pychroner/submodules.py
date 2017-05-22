# coding=utf-8
import importlib
import os
import sys

submodulesDir: str = "submodules"

def importModule(name: str) -> object:
    for directory in os.listdir(submodulesDir):
        sys.path.append(f"{os.getcwd()}/{submodulesDir}/{directory}")

    try:
        submodule: object = importlib.import_module(name)
        return submodule
    except:
        raise ImportError(f"No named submodule {name}")
