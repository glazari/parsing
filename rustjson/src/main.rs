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
    STRING(&'a str),
    NULL,
    BOOL(&'a str),
    ERROR(&'a str),
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

fn read_str(exp: &str, start_i: usize) -> (Token, usize) {
    let exb = exp.as_bytes();
    let (mut ch, mut i) = (exb[start_i], start_i + 1);
    while i < exb.len() && exb[i] != '\"' as u8 {
        i += 1
    }
    return (Token::STRING(&exp[start_i + 1..i]), i + 1);
}

#[cfg(test)]
#[test]
fn tokenize_str() {
    let tests = [
        ("\"a\"", Token::STRING("a"), 3),
        ("\"ab\"", Token::STRING("ab"), 4),
        ("\"abc\"", Token::STRING("abc"), 5),
    ];

    for test in tests.iter() {
        let (e, t, i) = test;
        let got = read_str(e, 0);
        assert_eq!(got, (t.clone(), *i));
    }
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
