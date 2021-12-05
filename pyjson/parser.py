from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type as ttype


@dataclass
class Error:
    msg: str


Value = int | str | List["Value"]


def parse_array(tokens: List[Token], i: int = 0) -> List[Value] | Error:
    out, i = [], i + 1
    if tokens[i].type == ttype.RBRACKET:
        return out

    val = parse_value(tokens, i)
    if isinstance(val, Error):
        return val
    out.append(val)
    i += 1

    while i < len(tokens) and tokens[i].type != ttype.RBRACKET:
        if tokens[i].type != ttype.COMMA:
            return Error("expecting comma")
        i += 1
        if i >= len(tokens):
            return Error("expected value after comma")
        val = parse_value(tokens, i)
        if isinstance(val, Error):
            return val
        out.append(val)
        i += 1
    if i > len(tokens):
        return Error("did not close array")
    return out


def parse_value(tokens: List[Token], i: int = 0) -> Value | Error:
    token = tokens[i]
    if token.type == ttype.NUM:
        return parse_num(token)
    elif token.type == ttype.STRING:
        return parse_str(token)
    elif token.type == ttype.LBRACKET:
        return parse_array(tokens, i)
    else:
        return Error(f"invalid token type {token}")
    pass


def parse_num(t: Token) -> int | Error:
    if t.type == ttype.ERROR:
        return Error(f"invalid num {t.value}")
    return float(t.value)


def parse_str(t: Token) -> str | Error:
    if t.type == ttype.ERROR:
        return Error(f"invalid str {t.value}")
    return t.value
