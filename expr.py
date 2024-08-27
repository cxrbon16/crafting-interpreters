from scanner import Token 

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
    
    def visit(self, interpreterC):
        return interpreterC.visitVariable(self) 

class Assignment(Expr):
    def __init__(self, name, val):
        self.lvalue = name
        self.rvalue = val 

    def visit(self, interpreterC):
        return interpreterC.visitAssignment(self)

class Binary(Expr):
    def  __init__(self, left, right, operator: Token):
        self.left = left
        self.right = right
        self.operator = operator

    def visit(self, interpreterC):
       return interpreterC.visitBinary(self) 

class Logical(Expr):
    def __init__(self, left, right, operator) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def visit(self, interpreterC):
        return interpreterC.visitLogical(self)


class Unary(Expr):
    def __init__(self, operator: Token, expr):
        self.operator: Token = operator
        self.expr = expr 

    def visit(self, interpreterC):
        return interpreterC.visitUnary(self)

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def visit(self, interpreterC):
        return interpreterC.visitGrouping(self)

class Literal(Expr):
    def __init__(self, val):
        self.value = val

    def visit(self, interpreterC):
        return interpreterC.visitLiteral(self)

