fn main() {
    println!("Hello, world!");
}

#[derive(Debug, PartialEq, Clone)]
enum Token {
    NUM(String),
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


fn read_num(exp: &str, i: usize) -> (Token, usize) {
    return (Token::EOF, 1);
}



#[cfg(test)]
#[test]
fn tokenize_num() {
    struct Test<'a> {
        e: &'a str,  // expression
        t: Token,    // output token
        i: usize,    // output char posistion
    }

    let tests = [
        Test{e: "1", t: Token::NUM("1".to_string()), i: 1},
    ];

    for  test in tests.iter() {
        let got = read_num(test.e, 0);
        assert_eq!(got, (test.t.clone(), test.i));

    }
}
