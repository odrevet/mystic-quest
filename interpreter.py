import ply.yacc as yacc
import ply.lex as lex

from script import read_scripts


class Variable:
    def __init__(self, name, id, value):
        self.name = name
        self.id = id
        self.value = value


variables = []
variable_declarations, scripts = read_scripts()
debug_tokens = False
game = None

def print_tokens(lexer):
    for tok in lexer:
        print(tok)

## Lexer ##
reserved = {
    "IF": "IF",
    # "ELSE": "ELSE",
    "END": "END",
    "let": "LET",
    "var": "VAR",
    # "FOR": "FOR",
    "FLAG_ON": "FLAG_ON",
    "FLAG_OFF": "FLAG_OFF",
    "CALL": "CALL",
}

tokens = [
    "ID",
    "HEX",
    "DOLLAR",
    # "EXCLAMATION",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "ASSIGN",
    "COMMA",
    "NEWLINE",
] + list(reserved.values())

t_HEX = r"[0-9a-f]+"
t_DOLLAR = r"\$"
# t_EXCLAMATION = r"\!"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_ASSIGN = r"="
t_COMMA = r"\,"

t_ignore = " "


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


## Parser ##
def p_program(p):
    """program : statement
    | program statement"""
    pass


def p_statement(p):
    """statement : function_call
    | call
    | variable_declaration
    | condition
    | flag
    | NEWLINE
    | END"""
    pass


# TODO named parameters dynamic repetition
def p_function_call(p):
    """function_call : ID
    | ID HEX
    | ID LPAREN ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX RPAREN
    | ID LPAREN ID COMMA ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX COMMA HEX RPAREN
    | ID LPAREN ID COMMA ID COMMA ID COMMA ID RPAREN ASSIGN LPAREN HEX COMMA HEX COMMA HEX COMMA HEX RPAREN"""
    try:
        f = getattr(game, p[1])
    except AttributeError:
        print(f"Function {p[1]} unimplemented")
        return

    if len(p) == 2:
        f()
    elif len(p) == 21:
        f(p[13], p[15], p[17], p[19])
    elif len(p) == 3:
        f(p[2])


def p_call(p):
    "call : CALL DOLLAR HEX"
    script = next(
        (script for script in scripts if script.id == p[3]),
        None,
    )

    if script is None:
        print(f"CALL: Script {p[3]} not found")
    else:
        lexer = lex.lex()
        if debug_tokens:
            lexer.input(script.instructions)
            print(script.instructions)
            print_tokens(lexer)
        parser = yacc.yacc()
        parser.parse(script.instructions)
        


def p_variable_declaration(p):
    """variable_declaration : LET ID ASSIGN VAR LBRACKET HEX RBRACKET"""
    variable = Variable(p[2], p[6], False)
    variables.append(variable)


def p_condition(p):
    "condition : IF LPAREN ID RPAREN"
    print(f"CONDITION {p[3]}")
    condition_is_true = next(
        (
            variable
            for variable in variables
            if (variable.name == p[3] and variable.value == True)
        ),
        False,
    )
    if condition_is_true:
        print("exec block")
    else:
        print("skip block")


def p_flag(p):
    """flag : FLAG_ON ID
    | FLAG_OFF ID"""
    variable = next(
        (variable for variable in variables if variable.name == p[2]),
        None,
    )

    if variable is None:
        print(f"{p[1]}: Variable {p[2]} not found")
    else:
        variable.value = p[1] == "FLAG_ON"


def p_error(p):
    print("Syntax error in input!")
