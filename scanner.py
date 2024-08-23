import sys
from enum import Enum

class TokenType(Enum): 
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    EQUAL = 12
    EQUAL_EQUAL = 13
    BANG = 14
    BANG_EQUAL = 15
    LESS = 16
    GREATER = 17
    LESS_EQUAL = 18
    GREATER_EQUAL = 19
    COMMENT = 20
    STRING = 21
    NUMBER = 22
    IDENTIFIER = 23
    AND = 24
    CLASS = 25
    ELSE = 26
    FALSE = 27
    FOR = 28
    FUN = 29
    IF = 30
    NIL = 31
    OR = 32
    PRINT = 33
    RETURN = 34
    SUPER = 35
    THIS = 36
    TRUE = 37
    VAR = 38
    WHILE = 39
    EOF = 40



class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: str):
            self.type = type
            self.lexeme = lexeme
            self.literal = literal
            
t_to_c = {
    TokenType.LEFT_PAREN: '(',
    TokenType.RIGHT_PAREN: ')',
    TokenType.LEFT_BRACE: '{',
    TokenType.RIGHT_BRACE: '}',
    TokenType.COMMA: ',',
    TokenType.DOT: '.',
    TokenType.MINUS: '-',
    TokenType.PLUS: '+',
    TokenType.STAR: '*',
    TokenType.SLASH: '/',
    TokenType.SEMICOLON: ';',
    TokenType.EQUAL: '=',
    TokenType.EQUAL_EQUAL: '==',
    TokenType.BANG: '!',
    TokenType.BANG_EQUAL: '!=',
    TokenType.LESS: '<',
    TokenType.GREATER: '>',
    TokenType.LESS_EQUAL: '<=',
    TokenType.GREATER_EQUAL: '>=',
    TokenType.COMMENT: '//',
    TokenType.STRING: '"',
    TokenType.NUMBER: '',
    TokenType.IDENTIFIER: '',
    TokenType.AND: 'and',
    TokenType.ELSE: 'else',
    TokenType.FALSE: 'false',
    TokenType.FOR: 'for',
    TokenType.FUN: 'fun',
    TokenType.IF: 'if',
    TokenType.NIL: 'nil',
    TokenType.OR: 'or',
    TokenType.PRINT: 'print',
    TokenType.RETURN: 'return',
    TokenType.SUPER: 'super',
    TokenType.THIS: 'this',
    TokenType.TRUE: 'true',
    TokenType.VAR: 'var',
    TokenType.WHILE: 'while',
}

c_to_t = dict()


for t, c in t_to_c.items():
    c_to_t.update({c: t})

pre_tokens = ['<', '>', '!', '=']

class Scanner:
    def __init__(self, source):
        self.source = source
        self.token_list = []
        self.error = False
        


    def add_token(self, TokenType, lexeme, literal):        
        self.token_list.append(Token(TokenType, lexeme, literal))
        


    def handle_string(self, start_idx):
        end_idx = self.source.find('"', start_idx + 1)
        if end_idx == -1:
            self.error = True
            line_number = self.source.count("\n", 0, start_idx) + 1
            print(
                f"[line {line_number}] Error: Unterminated string.",
                file=sys.stderr,
            )
            i = len(self.source)
            return i 
        else:

            str_lexeme = self.source[start_idx:end_idx+1]
            self.add_token(TokenType.STRING, str_lexeme, str_lexeme[1:-1])
            # self.add_token(TokenType.STRING, str_lexeme, str_lexeme.lstrip()) # 
            i = end_idx 
            return i
    
    

    def handle_nums(self, start_idx):
        idx = start_idx
        context = ""
        dotright = True

        while idx < len(self.source):
            lit = self.source[idx]
            if lit.isnumeric():
                context += lit
                idx += 1
            elif lit == "." and (idx + 1 < len(self.source)) and dotright:
                dotright = False
                context += lit
                idx += 1
            else:
                break
        self.add_token(TokenType.NUMBER, context, float(context))
        return idx - 1



    def handle_double_tokens(self):
        pass



    def handle_single_tokens(self):
        pass



    def handle_error(self):
        pass
    


    def is_identifer_char(self, char):
        char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
        return str(char) in char_set



    def is_whitespace(self, char_arr):
        if char_arr == ' ' or char_arr == '\t' or char_arr == '\n' or char_arr == '':
            return True



    def handle_identifiers(self, start_idx):

        i = start_idx
        char_arr = ''

        while i < len(self.source) and self.is_identifer_char(self.source[i]):
            char_arr += self.source[i]
            i += 1

        if char_arr in c_to_t:
            self.add_token(c_to_t[char_arr], char_arr, 'null')

        else:
            self.add_token(TokenType.IDENTIFIER, char_arr, 'null')

        return i - 1



    def tokenize(self): # refactor with more helper functions

        i = 0
        self.error = False


        while i < len(self.source):

            char:str = self.source[i]

            if self.is_whitespace(char):
                pass

            elif char == '"':
                i = self.handle_string(i)

            elif char.isnumeric():
                i = self.handle_nums(i)

            elif self.is_identifer_char(char):
                i = self.handle_identifiers(i)

            elif char not in c_to_t.keys():
                self.error = True
                line_number = self.source.count("\n", 0, i) + 1
                print(
                    f"[line {line_number}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )

            else:
                if char in pre_tokens:
                    if i+1<len(self.source) and self.source[i+1] == '=':
                        char += '=' 
                        i += 1
                        self.add_token(c_to_t[char], char, "null")
                    else:
                        self.add_token(c_to_t[char], char, "null")
                elif char == '/':
                    if i+1<len(self.source) and self.source[i+1] == '/':
                        while (i != len(self.source) and self.source[i] != '\n'):
                            i += 1
                    else:
                        self.add_token(c_to_t[char], char, "null")
                elif char in c_to_t:
                    self.add_token(c_to_t[char], char, "null")
            i += 1

        self.add_token(TokenType.EOF, '', "null")
        return not self.error

    def print_token_list(self):


        for t in self.token_list:
            print(f"{t.type.name} {t.lexeme} {t.literal}") 


