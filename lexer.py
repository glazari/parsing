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


def read_num(exp: str, i: int = 0) -> List[Token]:
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


def test_num():
    @dataclass
    class Test:
        exp: str
        token: Token
        i: int

        @property
        def out(self):
            return (self.token, self.i)

    tests = [
        Test("1", Token("1", Type.NUM), 1),
        Test("2", Token("2", Type.NUM), 1),
        Test("10", Token("10", Type.NUM), 2),
        Test("123", Token("123", Type.NUM), 3),
        Test("12.3", Token("12.3", Type.NUM), 4),
        Test("1.2.3", Token("1.2.", Type.ERROR), 3),
    ]

    for test in tests:
        got = read_num(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out


def test_lex():
    @dataclass
    class Test:
        exp: str
        out: List[Token]

    tests = [
        Test("1", [Token("1", Type.NUM), Token("", Type.EOF)]),
        Test("10", [Token("10", Type.NUM), Token("", Type.EOF)]),
        Test("10.2", [Token("10.2", Type.NUM), Token("", Type.EOF)]),
    ]

    for test in tests:
        got = lex(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
