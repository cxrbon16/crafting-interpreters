from expr import Assignment, Binary, Literal, Unary, Variable
from scanner import TokenType 
from stmt import varStmt, printStmt, exprStmt




class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.current = 0

# start: util functions 
            
    def match(self, types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def advance(self):
        
        self.current += 1

    def is_at_end(self):
        return self.token_list[self.current].type == TokenType.EOF

    def check(self, t):
        if self.is_at_end():
            return False
        return self.token_list[self.current].type == t

    def consume(self, t):
        if(self.check(t)):
            self.advance()
            return self.token_list[self.current - 1]

        print(f"{self.token_list[self.current].type} has found" )
        self.advance()
        raise Exception("We have an error")

# end: util functions

    def parse(self):
        # return a list of declaration:
        # declaration -> varDecl | statement
        # statement -> exprStatement | printStatement


        l_of_dec = []

        while(not self.is_at_end()):
            l_of_dec.append(self.declaration())

        return l_of_dec 


#statements

    def declaration(self):
        if (self.match([TokenType.VAR])):
            return self.var_declaration()
        else:
            return self.statement()

    def var_declaration(self):
        identifier = self.consume(TokenType.IDENTIFIER).lexeme
        initializer = None
        if (self.match([TokenType.EQUAL])):
           initializer = self.expression()
        self.consume(TokenType.SEMICOLON)
        return varStmt(identifier, initializer)

    def statement(self):
        if (self.match([TokenType.PRINT])):
            return self.print_statement()
        else:
            return self.expression_statement()
    
    def print_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON)
        return printStmt(expr)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON)
        return exprStmt(expr)

#expressions

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if (self.match([TokenType.EQUAL])):
            val = self.assignment()
            if (isinstance(expr, Variable)):
               name = expr.token_name
               return Assignment(name, val)

        return expr

    def equality(self):

        expr = self.comparison()
        while(self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):

            operator = self.token_list[self.current - 1]
            right = self.comparison()
            expr = Binary(expr, right, operator)
        return expr

    def comparison(self):
        expr = self.term()

        while(self.match([TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL])):
            operator = self.token_list[self.current - 1]
            right = self.term()
            expr = Binary(expr, right, operator)
        return expr

    def term(self):
        expr = self.factor()
        
        while(self.match([TokenType.PLUS, TokenType.MINUS])):
            operator = self.token_list[self.current - 1]
            right = self.factor()
            expr = Binary(expr, right, operator)
        return expr
    
    def factor(self):
        expr = self.unary()
        
        while(self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.token_list[self.current - 1]
            right = self.unary()
            expr = Binary(expr, right, operator)
        return expr 

    def unary(self):
        if(self.match([TokenType.BANG, TokenType.MINUS])):
            operator = self.token_list[self.current - 1]
            right = self.unary()
            return Unary(operator, right)
            
        return self.primary()

    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)

        if self.match([TokenType.TRUE]):
            return Literal(True)

        if self.match([TokenType.NIL]):
            return Literal(None)

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN)
            return expr

        if self.match([TokenType.IDENTIFIER]):
            return Variable(self.token_list[self.current - 1].lexeme)  

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.token_list[self.current - 1].literal)
