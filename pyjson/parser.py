from __future__ import annotations

from dataclasses import dataclass

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type as ttype


@dataclass
class Error:
    msg: str


Value = int | str | list["Value"]


def parse(string: str) -> Value:
    tokens = lexer.lex(string)
    val = parse_value(tokens)
    if isinstance(val, Error):
        raise Exception(val.msg)
    return val[0]


def parse_object(tokens: list[Token], i: int = 0) -> tuple[dict[Value], int] | Error:
    out, i = {}, i + 1
    if tokens[i].type == ttype.RBRACE:
        return out, i + 1

    def _key_pair(tokens, i, out) -> tuple[tuple[str, Value], int] | Error:
        key = parse_str(tokens[i])
        if isinstance(key, Error):
            return Error
        i += 1
        if i >= len(tokens) or tokens[i].type != ttype.COLON:
            return Error("expecting colon in object")
        val = parse_value(tokens, i + 1)
        if isinstance(key, Error):
            return Error

        v, i = val
        out[key] = v
        return i

    val = _key_pair(tokens, i, out)
    if isinstance(val, Error):
        return val
    i = val

    while i < len(tokens) and tokens[i].type != ttype.RBRACE:
        if tokens[i].type != ttype.COMMA:
            return Error("expecting comma")
        i += 1
        if i >= len(tokens):
            return Error("expected value after comma")
        val = _key_pair(tokens, i, out)
        if isinstance(val, Error):
            return val
        i = val
    if i > len(tokens):
        return Error("did not close object")
    return out, i + 1


def parse_array(tokens: list[Token], i: int = 0) -> tuple[list[Value], int] | Error:
    out, i = [], i + 1
    if tokens[i].type == ttype.RBRACKET:
        return out, i + 1

    val = parse_value(tokens, i)
    if isinstance(val, Error):
        return val
    out.append(val[0])
    i = val[1]

    while i < len(tokens) and tokens[i].type != ttype.RBRACKET:
        if tokens[i].type != ttype.COMMA:
            return Error("expecting comma")
        i += 1
        if i >= len(tokens):
            return Error("expected value after comma")
        val = parse_value(tokens, i)
        if isinstance(val, Error):
            return val
        out.append(val[0])
        i = val[1]
    if i > len(tokens):
        return Error("did not close array")
    return out, i + 1


def parse_value(tokens: list[Token], i: int = 0) -> tuple[Value, int] | Error:
    token = tokens[i]
    # print(i, token.value, [t.value for t in tokens])
    if token.type == ttype.NUM:
        val = parse_num(token)
        if isinstance(val, Error):
            return val
        return val, i + 1
    elif token.type == ttype.STRING:
        val = parse_str(token)
        if isinstance(val, Error):
            return val
        return val, i + 1
    elif token.type == ttype.LBRACKET:
        val = parse_array(tokens, i)
        if isinstance(val, Error):
            return val
        return val
    elif token.type == ttype.LBRACE:
        val = parse_object(tokens, i)
        if isinstance(val, Error):
            return val
        return val
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
