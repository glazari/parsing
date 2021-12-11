mod lexer;
mod parser;

fn main() {
    let out = lexer::lex("1 2 \"asdf\"", 0);
    println!("'{:?}", out);

    let out = parser::parse("12");
    println!("'{:?}", out);
}
