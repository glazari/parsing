from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

import pytest


@dataclass
class Token:
    value: str
    type: Type


class Type(Enum):
    NUM = "NUM"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    STRING = "STRING"
    NULL = "NULL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    ERROR = "ERROR"
    EOF = ""


def lex(exp: str, i: int = 0) -> List[Token]:
    if i >= len(exp):
        return [Token("", Type.EOF)]

    ch = exp[i]
    out = []
    if ch in set("0123456789"):
        num, i = read_num(exp, i)
        out.append(num)

    out.extend(lex(exp, i))
    return out


def read_num(exp: str, i: int = 0) -> Token:
    num = exp[i]
    i += 1
    point = False
    while i < len(exp) and exp[i] in set("0123456789."):
        if exp[i] == "." and point:
            return (Token(num + ".", Type.ERROR), i)  # syntax error
        point = point or exp[i] == "."
        num += exp[i]
        i += 1
    return (Token(num, Type.NUM), i)


def read_str(exp: str, i: int = 0) -> Token:
    string, i = "", i + 1
    while i < len(exp) and exp[i] != '"':
        string += exp[i]
        i += 1
    return (Token(string, Type.STRING), i + 1)
