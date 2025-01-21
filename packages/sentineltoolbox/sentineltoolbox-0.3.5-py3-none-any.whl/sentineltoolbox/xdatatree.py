__all__ = ["xDataTree", "xDataTreeType"]

from typing import Any, TypeAlias

from datatree import DataTree as xDataTree

xDataTreeType: TypeAlias = xDataTree[Any]
