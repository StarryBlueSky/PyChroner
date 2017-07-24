# coding=utf-8
import importlib
import os
import sys
from types import ModuleType

submodulesDir: str = "submodules"

def importModule(name: str) -> ModuleType:
    for directory in os.listdir(submodulesDir):
        sys.path.append(f"{submodulesDir}/{directory}")

    try:
        submodule: ModuleType = importlib.import_module(name)
        return submodule
    except:
        raise ImportError(f"No named submodule {name}")
