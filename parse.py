from __future__ import annotations

from dataclasses import dataclass

import pytest

import lexer
from lexer import Token
from lexer import Type as ttype


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


def test_num():
    @dataclass
    class Test:
        exp: str
        out: int

    tests = [
        Test("1", 1),
        Test("2", 2),
        Test("10", 10),
        Test("123", 123),
        Test("12.3", 12.3),
        Test("1.2.3", None),
    ]

    for test in tests:
        got = parse_num(lexer.read_num(test.exp)[0])
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
