import sys
from parser import Parser
from scanner import  Scanner
from expr import Expr
from interpreter import Interpreter

def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "parse":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
        scanner = Scanner(file_contents) 
        scanner.tokenize()
        parser = Parser(scanner.token_list)
        interpreter = Interpreter(parser.parse())        
        if scanner.tokenize():
            scanner.print_token_list()
            interpreter.interpret()
            exit(0)
        else:
            scanner.print_token_list()
            exit(65)

if __name__ == "__main__":
    main()
