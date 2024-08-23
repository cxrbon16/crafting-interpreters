from environment import Environment
from scanner import TokenType
env = Environment()


class Interpreter():
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
       
    def interpret(self):
        for stmt in self.stmt_list:
            stmt.evaluate()
        print(env.values)


# stmt funcs

def eval_printStmt(printStmt):
    val = printStmt.expression.visit()
    print(val)

def eval_exprStmt(exprStmt):
    return exprStmt.visit()

 
def eval_varStmt(varStmt):
    val = varStmt.expr.visit()
    env.define(varStmt.name, val)

# expr funcs

def visitVariable(varExpr):
    return env.get(varExpr.token_name)


def visitUnary(unaryExpr):
        def isTrue(object):
            if object is not None:
                return bool(object)
            return False

        right = None
        if unaryExpr.expr:
            right = unaryExpr.expr.visit()
        match(unaryExpr.operator.type):
            case(TokenType.MINUS):
                if right:
                    return -right
            case(TokenType.BANG):
                if right is not None:
                    return not isTrue(right) 
        return None 


def visitBinary(binaryExpr):
        left = binaryExpr.left.visit()
        right = binaryExpr.right.visit()

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

def visitGrouping(groupingExpr):
    return groupingExpr.expr.visit()

def visitLiteral(literalExpr):
    return literalExpr.value

