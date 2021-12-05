# call script by id or parse variable declaration if parameter is "vars"

import sys
import ply.lex as lex
import ply.yacc as yacc

from script import read_scripts
import function

variable_declarations, scripts = read_scripts()

nro_script = sys.argv[1]

instructions = ""

if nro_script == "vars":
    instructions = variable_declarations
else:
    script = next(
        (script for script in scripts if script.id == nro_script),
        None,
    )

    if script is None:
        sys.exit()

    instructions = script.instructions

print(instructions)


## Lexer ##
reserved = {
    "IF": "IF",
    "ELSE": "ELSE",
    "END": "END",
    "let": "LET",
    "var": "VAR",
    "FOR": "FOR",
}

tokens = [
    "HEX",
    "ID",
    "NEWLINE",
    "DOLLAR",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "ASSIGN",
    "COMMA",
] + list(reserved.values())

t_HEX = r"[0-9a-f]+"
t_DOLLAR = r"\$"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_ASSIGN = r"="
t_COMMA = r"\,"

t_ignore = " "


def t_ID(t):
    r"[A-Za-z_]+"
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

variables = {}

## Parser ##
def p_program(p):
    """program : function_call
    | program function_call
    | program NOOP
    | program NEWLINE"""
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


# def p_variable_declaration(p):
#    """variable_declaration : LET VARNAME ASSIGN VAR LBRACKET HEX RBRACKET"""
#    print("WIP Variable declaration")
#    print("TODO Add name (VARNAME) and identifier (HEX) in variable hash")


def p_error(p):
    print("Syntax error in input!")


# Display tokens
lexer.input(instructions)
for tok in lexer:
    print(tok)

# Parse and print result
parser = yacc.yacc()
result = parser.parse(instructions, debug=0)
print(result)
