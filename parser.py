from expr import Assignment, Binary, Literal, Logical, Unary, Variable, Call
from scanner import TokenType 
from stmt import blockStmt, varStmt, printStmt, exprStmt, ifStmt, whileStmt, forStmt

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

        elif(self.match([TokenType.LEFT_BRACE])):
            return blockStmt(self.block_statement())

        elif(self.match([TokenType.IF])):
            params = self.if_statement()
            return ifStmt(params[0], params[1], params[2])

        elif(self.match([TokenType.WHILE])):
            params = self.while_statement()
            return whileStmt(params[0], params[1])

        elif(self.match([TokenType.FOR])):
            params = self.for_statement()
            return forStmt(params[0], params[1], params[2], params[3])

        else:
            return self.expression_statement()

    def while_statement(self):
        cond = self.expression()
        block = self.declaration() 

        return [cond, block]

    def for_statement(self):

        self.consume(TokenType.LEFT_PAREN)
        dec = self.declaration()
        cond = self.expression()
        self.consume(TokenType.SEMICOLON)
        stmt = self.expression()
        self.consume(TokenType.RIGHT_PAREN)

        block = self.statement()
        
        return [dec, cond, stmt, block]


    def if_statement(self):
        condition = self.expression()
        if_block = self.declaration()  
        else_block = None

        if(self.match([TokenType.ELSE])):
            else_block = self.declaration()

        return [condition, if_block, else_block] 

    def block_statement(self):
        stmts = []
        while(not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end()):
            stmts.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE)
        return stmts


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
        expr = self.logical_or()
        if (self.match([TokenType.EQUAL])):
            val = self.assignment()
            if (isinstance(expr, Variable)):
               name = expr.token_name
               return Assignment(name, val)

        return expr

    def logical_or(self):
        left = self.logical_and()

        while self.match([TokenType.OR]):
            operator = self.token_list[self.current - 1]
            right = self.logical_and()
            left = Logical(left, right, operator)

        return left

    def logical_and(self):
        left = self.equality()

        while(self.match([TokenType.AND])):
            operator = self.token_list[self.current - 1]
            right = self.equality()
            left = Logical(left, right, operator)

        return left



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
        
        while(self.match([TokenType.SLASH, TokenType.STAR, TokenType.PERCENT])):
            operator = self.token_list[self.current - 1]
            right = self.unary()
            expr = Binary(expr, right, operator)
        return expr 

    def unary(self):
        if(self.match([TokenType.BANG, TokenType.MINUS])):
            operator = self.token_list[self.current - 1]
            right = self.unary()
            return Unary(operator, right)
            
        return self.call()

    def finish_call(self, expr):

        args = []

        if(not self.match([TokenType.RIGHT_PAREN])):
            while(self.match([TokenType.COMMA])):
                args.append(self.token_list[self.current])
                self.current = self.current + 1

        return Call(expr, args)

    def call(self):
        expr = self.primary()
        
        while(True):
            if(self.match([TokenType.LEFT_PAREN])):
                expr = self.finish_call(expr)
            else:
                break

        return expr

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
