mod lexer;
mod parser;

fn main() {
    let exp = r#"{
        "this": "that",
        "list": [1,2,3],
        "obj": {"false": false},
        "true": true,
        "null": null
    }"#;

    let out = lexer::lex(exp, 0);
    println!("'{:?}", out);

    let out = parser::parse(exp);
    println!("'{:?}", out);
}
