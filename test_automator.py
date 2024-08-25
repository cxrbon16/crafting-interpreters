from parser import Parser
from interpreter import Interpreter
from scanner import Scanner

example_inputs = ["print 12 + 13;"]

example_outputs = [True]


for ind in range(len(example_inputs)):

    inp = input("write an statement: ")


    scanner = Scanner(inp)
    scanner.tokenize()
    for t in scanner.token_list:
        print(t.lexeme)
    parser = Parser(scanner.token_list) 
    interpreter = Interpreter(parser.parse()) 
    interpreter.interpret()
