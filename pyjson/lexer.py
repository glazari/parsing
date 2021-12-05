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
    COLON = ":"
    STRING = "STRING"
    NULL = "NULL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    ERROR = "ERROR"
    EOF = ""


def lex(exp: str, i: int = 0) -> List[Token]:
    i = skip_whitespace(exp, i)

    if i >= len(exp):
        return [Token("", Type.EOF)]

    ch = exp[i]
    out = []
    if ch in set("0123456789"):
        num, i = read_num(exp, i)
        out.append(num)
    elif ch == '"':
        string, i = read_str(exp, i)
        out.append(string)
    elif ch == "{":
        out.append(Token("{", Type.LBRACE))
        i += 1
    elif ch == "}":
        out.append(Token("}", Type.RBRACE))
        i += 1
    elif ch == "[":
        out.append(Token("[", Type.LBRACKET))
        i += 1
    elif ch == "]":
        out.append(Token("]", Type.RBRACKET))
        i += 1
    elif ch == ":":
        out.append(Token(":", Type.COLON))
        i += 1
    elif ch == ",":
        out.append(Token(",", Type.COMMA))
        i += 1
    elif ch == "t" and exp[i : i + 4] == "true":
        out.append(Token("true", Type.TRUE))
        i += 4
    elif ch == "f" and exp[i : i + 5] == "false":
        out.append(Token("false", Type.FALSE))
        i += 5
    else:
        err = f"unexpected: '{ch}' at pos {i}"
        out.append(Token(err, Type.ERROR))
        return out

    out.extend(lex(exp, i))
    return out


def skip_whitespace(exp: str, i: int = 0) -> int:
    while i < len(exp) and exp[i] in set(" \n\t"):
        i += 1
    return i


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
