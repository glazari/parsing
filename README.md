# parsing
Exploring parsing of different things in different languages

# JSON parsers

json is a pretty simple data format so its a nice start for a parser.

## GRAMMAR

Below is a simplified version of the json grammar that I am using.

```
expression : value
value      : string | number | array | object | bool | null
array      : '[' value [ ',' value ] ']'
object     : '{' obj_val [ ',' obj_val ] '}'
obj_val    : string ':' value
string     : '"' LETTER* '"'
number     : DIGIT+ [ '.' DIGIT+ ]+
bool       : 'true' | 'false'
null       : 'null'
```

A more detailed version can  be found at https://www.json.org/json-en.html


## Python version

To test the python version install pytest `pip install pytest` and run it like so:

```bash
pytest pytests
```
