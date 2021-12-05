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
    return (Node(exp[i]), i + 1)


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
