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
    ERROR(String),
    EOF,
}

fn read_num(exp: &str, start_i: usize) -> (Token, usize) {
    let exb = exp.as_bytes();
    let mut i = start_i + 1;
    while i < exb.len() && exb[i].is_ascii_digit() {
        i = i + 1;
    }

    return (Token::NUM(&exp[start_i..i]), i);
}

fn read_str(exp: &str, start_i: usize) -> (Token, usize) {
    let exb = exp.as_bytes();
    let mut i = start_i + 1;
    while i < exb.len() && exb[i] != '\"' as u8 {
        i += 1
    }
    return (Token::STRING(&exp[start_i + 1..i]), i + 1);
}

fn skip_whitespace(exp: &str, start_i: usize) -> usize {
    let (exb, mut i) = (exp.as_bytes(), start_i);
    while i < exb.len() && exb[i].is_ascii_whitespace() {
        i += 1
    }
    return i;
}

fn read_non_whitespace(exp: &str, start_i: usize) -> (&str, usize) {
    let (exb, mut i) = (exp.as_bytes(), start_i);
    while i < exb.len() && !exb[i].is_ascii_whitespace() {
        i += 1
    }
    return (&exp[start_i..i], i);
}

fn lex(exp: &str, start_i: usize) -> Vec<Token> {
    let i = skip_whitespace(exp, start_i);
    let exb = exp.as_bytes();

    if i >= exb.len() {
        return [Token::EOF].to_vec();
    }

    let ch = exb[i];
    let (token, i) = match ch as char {
        '0'..='9' => read_num(exp, i),
        '"' => read_str(exp, i),
        '{' => (Token::LBRACE, i + 1),
        '}' => (Token::RBRACE, i + 1),
        '[' => (Token::LBRACKET, i + 1),
        ']' => (Token::RBRACKET, i + 1),
        ':' => (Token::COLON, i + 1),
        ',' => (Token::COMMA, i + 1),
        _ => {
            let (word, i) = read_non_whitespace(exp, i);
            match word {
                "true" | "false" => (Token::BOOL(word), i),
                "null" => (Token::NULL, i),
                _ => {
                    return vec![Token::ERROR(format!(
                        "unexpected token {} at pos {}",
                        ch as char, i
                    ))]
                }
            }
        }
    };
    let mut out: Vec<Token> = vec![token];

    out.extend(lex(exp, i));

    return out;
}

#[cfg(test)]
#[test]
fn test_lex() {
    let tests = [
        ("  ", vec![Token::EOF]),
        (" 1 ", vec![Token::NUM("1"), Token::EOF]),
        ("\"a\"", vec![Token::STRING("a"), Token::EOF]),
        (
            "1 \"a\" ",
            vec![Token::NUM("1"), Token::STRING("a"), Token::EOF],
        ),
        ("{", vec![Token::LBRACE, Token::EOF]),
        ("}", vec![Token::RBRACE, Token::EOF]),
        ("[", vec![Token::LBRACKET, Token::EOF]),
        ("]", vec![Token::RBRACKET, Token::EOF]),
        (":", vec![Token::COLON, Token::EOF]),
        (",", vec![Token::COMMA, Token::EOF]),
        ("true", vec![Token::BOOL("true"), Token::EOF]),
        ("false", vec![Token::BOOL("false"), Token::EOF]),
        ("null", vec![Token::NULL, Token::EOF]),
    ];

    for test in tests.iter() {
        let (e, v) = test;
        let got = lex(e, 0);
        assert_eq!(got, v.clone(), "{}", e);
    }
}

#[cfg(test)]
#[test]
fn test_read_non_whitespace() {
    let tests = [
        ("true ", "true", 4),
        ("false ", "false", 5),
        ("null ", "null", 4),
        ("asdfasdf\n\t  ", "asdfasdf", 8),
        ("%#$@()", "%#$@()", 6),
    ];

    for test in tests.iter() {
        let (e, t, i) = test;
        let got = read_non_whitespace(e, 0);
        assert_eq!(got, (*t, *i));
    }
}

#[cfg(test)]
#[test]
fn test_skip_whitespace() {
    let tests = [(" a", 1), ("  v", 2), ("   k", 3), ("a   k", 0)];

    for test in tests.iter() {
        let (e, i) = test;
        let got = skip_whitespace(e, 0);
        assert_eq!(got, *i, "{}", e);
    }
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
