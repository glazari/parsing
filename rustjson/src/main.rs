use std::char;

fn main() {
    println!("Hello, world!");
}

#[derive(Debug, PartialEq, Clone)]
enum Token<'a> {
    NUM(&'a str),
    LBRACE,
    RBRACE,
    LBRACKET,
    RBRACKET,
    COMMA,
    COLON,
    STRING(String),
    NULL,
    BOOL(String),
    ERROR(String),
    EOF,
}

fn read_num(exp: &str, start_i: usize) -> (Token, usize) {
    let exb = exp.as_bytes();
    let mut ch = exb[start_i];
    let mut i = start_i + 1;
    while i < exb.len() && exb[i].is_ascii_digit() {
        ch = exb[i];
        i = i + 1;
    }

    return (Token::NUM(&exp[start_i..i]), i);
}

#[cfg(test)]
#[test]
fn tokenize_num() {
    let tests = [
        ("1", Token::NUM("1"), 1),
        ("2", Token::NUM("2"), 1),
        ("21", Token::NUM("21"), 2),
        ("123", Token::NUM("123"), 3),
    ];

    for test in tests.iter() {
        let (e, t, i) = test;
        let got = read_num(e, 0);
        assert_eq!(got, (t.clone(), *i));
    }
}
