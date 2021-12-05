from __future__ import annotations

from typing import List

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type as ttype


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
