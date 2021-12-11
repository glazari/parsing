use crate::lexer::{self, Token};

#[derive(Debug, PartialEq, Clone)]
pub enum Value<'a> {
    NUM(f32),
    STR(&'a str),
    ARR(Vec<Value<'a>>),
}

#[derive(Debug, PartialEq, Clone)]
enum Error {
    NotANumber(String),
    UnexpectedToken(String),
    ExpectedValueAfterComma,
    UnclosedArray,
    E,
}

pub fn parse(string: &str) -> Value {
    let tokens = lexer::lex(string, 0);
    let (val, _) = parse_value(&tokens, 0).expect("Invalid Json");
    return val;
}

fn parse_value<'a>(tokens: &Vec<Token<'a>>, i: usize) -> Result<(Value<'a>, usize), Error> {
    let token = &tokens[i];
    match token {
        Token::NUM(_) => parse_num(token).map(|num| (Value::NUM(num), i + 1)),
        Token::STRING(s) => Ok((Value::STR(s), i + 1)),
        Token::LBRACKET => parse_array(tokens, i).map(|(arr, i)| (Value::ARR(arr), i)),
        _ => panic!("Unexpected token: {:?}", token),
    }
}

fn parse_num<'a>(t: &'a Token<'a>) -> Result<f32, Error> {
    let s = match t {
        Token::NUM(x) => x,
        _ => return Err(Error::NotANumber(t.to_string())),
    };
    return s.parse().map_err(|_| Error::NotANumber(t.to_string()));
}

fn parse_array<'a>(tokens: &Vec<Token<'a>>, i: usize) -> Result<(Vec<Value<'a>>, usize), Error> {
    let (mut out, i) = (vec![], i + 1);

    if tokens[i] == Token::RBRACKET {
        return Ok((out, i + 1));
    }

    let (val, i) = parse_value(tokens, i)?;
    out.push(val);
    let mut loop_i = i;
    while loop_i < tokens.len() && tokens[loop_i] != Token::RBRACKET {
        if tokens[loop_i] != Token::COMMA {
            return Err(Error::UnexpectedToken(tokens[loop_i].to_string()));
        }
        loop_i += 1;
        if loop_i >= tokens.len() {
            return Err(Error::ExpectedValueAfterComma);
        }
        let (val, i) = parse_value(tokens, loop_i)?;
        out.push(val);
        loop_i = i;
    }
    if loop_i >= tokens.len() {
        return Err(Error::UnclosedArray);
    }

    return Ok((out, loop_i + 1));
}

#[cfg(test)]
#[test]
fn test_array() {
    let tests = [
        ("[]", vec![], 2),
        ("[1]", vec![Value::NUM(1.)], 3),
        ("[1,2]", vec![Value::NUM(1.), Value::NUM(2.)], 5),
        (
            "[1,[4, 5]]",
            vec![
                Value::NUM(1.),
                Value::ARR(vec![Value::NUM(4.), Value::NUM(5.)]),
            ],
            9,
        ),
    ];

    for test in tests.iter() {
        let (e, out, i) = test;
        let (got, got_i) = parse_array(&lexer::lex(e, 0), 0).expect("test case failed");
        assert_eq!(*out, got, "{}", e);
        assert_eq!(*i, got_i, "{}", e);
    }
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

#[cfg(test)]
#[test]
fn test_parse() {
    let tests = [
        ("1", Value::NUM(1.)),
        ("21", Value::NUM(21.)),
        ("123", Value::NUM(123.)),
        (" \"asdf\"  ", Value::STR("asdf")),
        (
            "[1,2,3]",
            Value::ARR(vec![Value::NUM(1.), Value::NUM(2.), Value::NUM(3.)]),
        ),
    ];

    for test in tests.iter() {
        let (e, out) = test;
        let got = parse(e);
        assert_eq!(*out, got);
    }
}
