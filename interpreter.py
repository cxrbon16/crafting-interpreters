from environment import Environment
from scanner import TokenType


class Interpreter():
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
        global_env = Environment(None)
        self.env = global_env
       
    def interpret(self):
        for stmt in self.stmt_list:
            stmt.evaluate(self)


    # stmt funcs

    def eval_printStmt(self, printStmt):
        val = printStmt.expression.visit(self)
        print(val)

    def eval_blockStmt(self, blockStmt):
        prev = self.env 
        self.env = Environment(prev)
        for stmt in blockStmt.statements:
            stmt.evaluate(self)
        self.env = prev 
    def eval_exprStmt(self, exprStmt):
        return exprStmt.expression.visit(self)

     
    def eval_varStmt(self, varStmt):
        val = varStmt.expr.visit(self)
        self.env.define(varStmt.name, val)

    # expr funcs

    def visitVariable(self, varExpr):
        return self.env.get(varExpr.token_name)

    def visitAssignment(self, assignExpr):
        name = assignExpr.lvalue
        val = assignExpr.rvalue.visit(self)
        self.env.assign(name, val)
        return val

    def visitUnary(self, unaryExpr):
            def isTrue(object):
                if object is not None:
                    return bool(object)
                return False

            right = None
            if unaryExpr.expr:
                right = unaryExpr.expr.visit(self)
            match(unaryExpr.operator.type):
                case(TokenType.MINUS):
                    if right:
                        return -right
                case(TokenType.BANG):
                    if right is not None:
                        return not isTrue(right) 
            return None 


    def visitBinary(self, binaryExpr):
            left = binaryExpr.left.visit(self)
            right = binaryExpr.right.visit(self)

            match(binaryExpr.operator.type):

                case(TokenType.MINUS):
                    return left - right 

                case(TokenType.PLUS): # add string concatenate
                    if(isinstance(left, float) and isinstance(right, float)):
                        return right + left 
                    elif(isinstance(left, str) and isinstance(right, str)):
                        return right + left 

                case(TokenType.STAR):
                    if(isinstance(left, float) and isinstance(right, float)):
                        return right * left 
                    elif(isinstance(left, str) and isinstance(right, int)):
                        return left * right 
                    elif(isinstance(left, int) and isinstance(right, str)):
                        return left * right 

                case(TokenType.SLASH):
                    return left / right

                case(TokenType.GREATER):
                    return left > right 
               
                case(TokenType.GREATER_EQUAL):
                    return left >= right 

                case(TokenType.EQUAL_EQUAL):
                    return left == right

                case(TokenType.LESS):
                    return left < right

                case(TokenType.LESS_EQUAL):
                    return left <= right

                case(TokenType.LESS_EQUAL):
                    return left <= right

    def visitGrouping(self, groupingExpr):
        return groupingExpr.expr.visit(self)

    def visitLiteral(self, literalExpr):
        return literalExpr.value

