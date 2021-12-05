from __future__ import annotations

from dataclasses import dataclass

import pytest

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type as ttype


@dataclass
class Node:
    value: str
    left: Node = None
    right: Node = None


def parse(exp: str, i: int = 0) -> Node:
    pass


def parse_num(t: Token) -> int:
    if t.type == ttype.ERROR:
        return None
    return float(t.value)
