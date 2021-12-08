import sys
import argparse
import ply.lex as lex
import ply.yacc as yacc

from script import read_scripts
import function

class Variable:
    def __init__(self, name, id, value):
        self.name = name
        self.id = id
        self.value = value

parser = argparse.ArgumentParser()
parser.add_argument("--script")
parser.add_argument('--variable', dest='variable', action='store_true')
parser.set_defaults(variable=False)
args = parser.parse_args()

variable_declarations, scripts = read_scripts()

script = None
if args.script is not None:
    script = next(
        (script for script in scripts if script.id == args.script),
        None,
    )

    if script is None:
        print(f"Script {args.script} not found")
    else:
        print(script.instructions)


## Lexer ##
reserved = {
    "IF": "IF",
    #"ELSE": "ELSE",
    #"END": "END",
    "let": "LET",
    "var": "VAR",
    #"FOR": "FOR",
    "SET_ON" : "SET_ON",
    "SET_OFF" : "SET_OFF"
}

tokens = [
    "ID",
    "HEX",
    "DOLLAR",
    #"EXCLAMATION",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "ASSIGN",
    "COMMA",
    "NEWLINE"
] + list(reserved.values())

t_HEX = r"[0-9a-f]+"
t_DOLLAR = r"\$"
#t_EXCLAMATION = r"\!"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_ASSIGN = r"="
t_COMMA = r"\,"

t_ignore = " "


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
start = "program"

variables = []

## Parser ##
def p_program(p):
    """program : statement
    | program statement"""
    pass

def p_statement(p):
    """statement : function_call
    | variable_declaration
    | condition
    | set
    | NEWLINE"""
    pass

# TODO named parameters dynamic repetition
def p_function_call(p):
    """function_call : ID
    | ID HEX
    | ID DOLLAR HEX
    | ID LPAREN ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX RPAREN
    | ID LPAREN ID COMMA ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX COMMA HEX RPAREN
    | ID LPAREN ID COMMA ID COMMA ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX COMMA HEX COMMA HEX RPAREN"""
    try:
        f = getattr(function, p[1])
    except AttributeError:
        print(f"Function {p[1]} unimplemented")
        return

    if len(p) == 2:
        f()
    elif len(p) == 21:
        f(p[13], p[15], p[17], p[19])
    elif len(p) == 3:
        if p[2] == "$":
            f(p[3])
        else:
            f(p[2])


def p_variable_declaration(p):
   """variable_declaration : LET ID ASSIGN VAR LBRACKET HEX RBRACKET"""
   variable = Variable(p[2], p[6], False)
   variables.append(variable)


def p_condition(p):
    "condition : IF LPAREN ID RPAREN"
    condition_is_true = next(
        (variable for variable in variables if (variable.name == p[3] and variable.value == True)),
        False,
    )
    if(condition_is_true):
        print("exec block")
    else:
        print("skip block")


def p_set(p):
    """set : SET_ON ID
           | SET_OFF ID"""
    variable = next(
        (variable for variable in variables if variable.name == p[2]),
        None,
    )

    if variable is None:
        print(f"Warning: Variable {p[2]} not found when call to {p[1]}")
    else:
        variable.value = p[1] == "SET_ON"


def p_error(p):
    print("Syntax error in input!")


# Parse and print result
parser = yacc.yacc()

if args.variable:
    lexer.input(variable_declarations)
    for tok in lexer:
        print(tok)

    parser.parse(variable_declarations)

if script is not None:
    lexer.input(script.instructions)
    for tok in lexer:
        print(tok)

    result = parser.parse(script.instructions)
    print(result)
