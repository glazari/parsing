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
        Test(" 1", [Token("1", Type.NUM), Token("", Type.EOF)]),
        Test('  "this"  ', [Token("this", Type.STRING), Token("", Type.EOF)]),
        Test(
            '3  "this"  ',
            [Token("3", Type.NUM), Token("this", Type.STRING), Token("", Type.EOF)],
        ),
        Test("{", [Token("{", Type.LBRACE), Token("", Type.EOF)]),
        Test("}", [Token("}", Type.RBRACE), Token("", Type.EOF)]),
        Test("[", [Token("[", Type.LBRACKET), Token("", Type.EOF)]),
        Test("]", [Token("]", Type.RBRACKET), Token("", Type.EOF)]),
        Test(",", [Token(",", Type.COMMA), Token("", Type.EOF)]),
        Test("true", [Token("true", Type.TRUE), Token("", Type.EOF)]),
        Test("false", [Token("false", Type.FALSE), Token("", Type.EOF)]),
        Test(":", [Token(":", Type.COLON), Token("", Type.EOF)]),
    ]

    for test in tests:
        got = lexer.lex(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out


def test_skip_whitespace():
    @dataclass
    class Test:
        exp: str
        i: int
        out: int

    tests = [
        Test("  1", 0, 2),
        Test(" \n1", 0, 2),
        Test(" \t1", 0, 2),
    ]

    for test in tests:
        got = lexer.skip_whitespace(test.exp, test.i)
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


def test_str():
    @dataclass
    class Test:
        exp: str
        token: Token
        i: int

        @property
        def out(self):
            return (self.token, self.i)

    tests = [
        Test('"a"', Token("a", Type.STRING), 3),
        Test('"a"', Token("a", Type.STRING), 3),
    ]

    for test in tests:
        got = lexer.read_str(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
