from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pyjson import lexer
from pyjson.lexer import Token
from pyjson.lexer import Type


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
        got = lexer.lex(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out


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
        got = lexer.read_num(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
