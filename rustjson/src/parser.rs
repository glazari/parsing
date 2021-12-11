use crate::lexer::{self, Token};

#[derive(Debug, PartialEq, Clone)]
pub enum Value {
    NUM(f32),
}

#[derive(Debug, PartialEq, Clone)]
enum Error {
    NotANumber(String),
}

pub fn parse(string: &str) -> Value {
    let tokens = lexer::lex(string, 0);
    let (val, _) = parse_value(tokens, 0).expect("Invalid Json");
    return val;
}

fn parse_value(tokens: Vec<Token>, i: usize) -> Result<(Value, usize), Error> {
    let token = &tokens[i];
    match token {
        Token::NUM(_) => match parse_num(token) {
            Ok(num) => Ok((Value::NUM(num), i + 1)),
            Err(e) => Err(e),
        },
        _ => panic!("hi"),
    }
}

#[cfg(test)]
#[test]
fn test_parse() {
    let tests = [
        ("1", Value::NUM(1.)),
        ("21", Value::NUM(21.)),
        ("123", Value::NUM(123.)),
    ];

    for test in tests.iter() {
        let (e, out) = test;
        let got = parse(e);
        assert_eq!(*out, got);
    }
}

fn parse_num<'a>(t: &'a Token<'a>) -> Result<f32, Error> {
    let s = match t {
        Token::NUM(x) => x,
        _ => return Err(Error::NotANumber(t.to_string())),
    };
    return s.parse().map_err(|_| Error::NotANumber(t.to_string()));
}

#[cfg(test)]
#[test]
fn test_parse_num() {
    let tests = [("1", Ok(1.)), ("21", Ok(21.)), ("123", Ok(123.))];

    for test in tests.iter() {
        let (e, out) = test;
        let token = &lexer::lex(e, 0)[0];
        let got = parse_num(token);
        assert_eq!(*out, got);
    }
}
