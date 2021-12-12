import argparse
import readline
import ply.lex as lex
import ply.yacc as yacc

from interpreter import *

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--script", help="Script number to call")
    argparser.add_argument(
        "--skip-var",
        dest="parse_variable_declaration",
        action="store_false",
        help="Skip variable declaration",
    )
    argparser.set_defaults(parse_variable_declaration=True)
    argparser.add_argument(
        "--repl",
        dest="repl",
        action="store_true",
        help="Open a repl",
    )
    argparser.set_defaults(repl=False)
    argparser.add_argument(
        "--debug-tokens",
        dest="debug_tokens",
        action="store_true",
        help="Print lexer tokens",
    )
    argparser.set_defaults(debug_tokens=False)
    args = argparser.parse_args()

    debug_tokens = args.debug_tokens

    lexer = lex.lex()
    parser = yacc.yacc()

    if args.parse_variable_declaration:
        if debug_tokens:
            lexer.input(variable_declarations)
            print_tokens(lexer)
        parser.parse(variable_declarations)


    if args.script is not None:
        parser.parse(f"CALL ${args.script}")

    if args.repl:
        while True:
            try:
                instructions = input("> ")
            except EOFError:
                break
            if not instructions:
                continue
            if debug_tokens:
                lexer.input(instructions)
                print_tokens(lexer)
            parser.parse(instructions)
