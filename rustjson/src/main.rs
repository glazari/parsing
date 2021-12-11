mod lexer;
mod parser;

fn main() {
    let out = lexer::lex("1 2 \"asdf\"", 0);
    println!("'{:?}", out);

    let out = parser::parse(
        r#"{
        "this": "that",
        "list": [1,2,3],
        "obj": {"false": 1},
        "true": 3
    }"#,
    );
    println!("'{:?}", out);
}
