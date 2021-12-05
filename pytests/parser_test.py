from dataclasses import dataclass

from pyjson import lexer
from pyjson import parser


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
        got = parser.parse_num(lexer.read_num(test.exp)[0])
        if not got == test.out:
            print("test:", test.exp)
            print("exp:", test.out)
            print("got:", got)
            print()
        assert got == test.out
