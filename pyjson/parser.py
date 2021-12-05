from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type as ttype


@dataclass
class Error:
    msg: str


def parse_array(tokens: List[Token], i: int = 0) -> List(int | str) | Error:
    out, i = [], i + 1
    if tokens[i].type == ttype.RBRACKET:
        return out

    val = parse_value(tokens, i)
    if isinstance(val, str) and "ERROR" in val:
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
        if isinstance(val, str) and "ERROR" in val:
            return val
        out.append(val)
        i += 1
    if i > len(tokens):
        return Error("did not close array")
    return out


def parse_value(tokens: List[Token], i: int = 0) -> int | str:
    token = tokens[i]
    if token.type == ttype.NUM:
        return parse_num(token)
    elif token.type == ttype.STRING:
        return parse_str(token)
    else:
        return f"ERROR: invalid token type {token}"
    pass


def parse_num(t: Token) -> int:
    if t.type == ttype.ERROR:
        return None
    return float(t.value)


def parse_str(t: Token) -> str:
    if t.type == ttype.ERROR:
        return None
    return t.value
