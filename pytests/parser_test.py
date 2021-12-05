from dataclasses import dataclass

from pyjson import lexer
from pyjson import parser


def test_parse_array():
    @dataclass
    class Test:
        exp: str
        val: list[int | str]
        i: int

        @property
        def out(self):
            return self.val, self.i

    tests = [
        Test("[]", [], 2),
        Test("[1]", [1], 3),
        Test("[1,2]", [1, 2], 5),
        Test('["t",2]', ["t", 2], 5),
        Test("[1,2,[3]]", [1, 2, [3]], 9),
    ]

    for test in tests:
        got = parser.parse_array(lexer.lex(test.exp))
        assert_eq(test, got)


def test_parse_value():
    @dataclass
    class Test:
        exp: str
        val: int | str
        i: int

        @property
        def out(self):
            return self.val, self.i

    tests = [
        Test("1", 1, 1),
        Test('"this"', "this", 1),
        Test('["this", 1]', ["this", 1], 5),
    ]

    for test in tests:
        print("*" * 40)
        got = parser.parse_value(lexer.lex(test.exp))
        assert_eq(test, got)


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
        Test("1.2.3", parser.Error("invalid num 1.2.")),
    ]

    for test in tests:
        got = parser.parse_num(lexer.read_num(test.exp)[0])
        assert_eq(test, got)


def test_str():
    @dataclass
    class Test:
        exp: str
        out: int

    tests = [
        Test('"this"', "this"),
        Test('"that"', "that"),
        Test('"asdfasdf"', "asdfasdf"),
    ]

    for test in tests:
        got = parser.parse_str(lexer.read_str(test.exp)[0])
        assert_eq(test, got)


def assert_eq(test, got):
    if not got == test.out:
        print("test:", test.exp)
        print("exp:", test.out)
        print("got:", got)
        print()
    assert got == test.out
