mod lexer;

fn main() {
    let out = lexer::lex("1 2 \"asdf\"", 0);
    println!("'{:?}", out);
}
