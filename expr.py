from scanner import Token 
import interpreter

class Expr():
    def __init__(self):
        pass



def paranthesize(exprs):
    res = "( "

    for val in exprs:
        res += str(val.visit()) + " " 
    return res + ")"


class Variable(Expr):
    def __init__(self, token_name):
        self.token_name = token_name
    
    def visit(self):
        return interpreter.visitVariable(self) 

        

class Binary(Expr):
    def __init__(self, left, right, operator: Token):
        self.left = left
        self.right= right
        self.operator = operator

    def visit(self):
       return interpreter.visitBinary(self) 

class Unary(Expr):
    def __init__(self, operator: Token, expr):
        self.operator: Token = operator
        self.expr = expr 

    def visit(self):
        return interpreter.visitUnary(self)

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return interpreter.visitGrouping(self)

class Literal(Expr):
    def __init__(self, val):
        self.value = val

    def visit(self):
        return interpreter.visitLiteral(self)

