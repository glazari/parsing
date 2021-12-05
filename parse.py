from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass
class Node:
    value: str
    left: Node = None
    right: Node = None


def parse(exp: str, i: int = 0) -> Node:
    ch = exp[i]
    if ch in set("0123456789"):
        numNode, i = parse_num(exp, i)

    return Node(None)


def parse_num(exp: str, i: int = 0) -> (Node, int):
    num = exp[i]
    i += 1
    point = False
    while i < len(exp) and exp[i] in set("0123456789."):
        if exp[i] == "." and point:
            return (Node(None), i)  # syntax error
        point = point or exp[i] == "."
        num += exp[i]
        i += 1
    return (Node(num), i)


def test_num():
    @dataclass
    class Test:
        exp: str
        node: Node
        i: int

        @property
        def out(self):
            return (self.node, self.i)

    tests = [
        Test("1", Node("1"), 1),
        Test("2", Node("2"), 1),
        Test("10", Node("10"), 2),
        Test("123", Node("123"), 3),
        Test("12.3", Node("12.3"), 4),
        Test("1.2.3", Node(None), 3),
    ]

    for test in tests:
        got = parse_num(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out


@pytest.mark.skip()
def test_parse():
    @dataclass
    class Test:
        exp: str
        out: Node

    tests = [
        Test("1+2", Node("+", Node(1), Node(2))),
    ]

    for test in tests:
        got = parse(test.exp)
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
