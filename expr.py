from scanner import Token, TokenType 



class Expr():
    def __init__(self):
        pass


class Variable(Expr):
    def __init__(self, token_name):
        self.token_name = token_name
    
    def visit(self):
        return "variable"
        
        

def paranthesize(exprs):
    res = "( "

    for val in exprs:
        res += str(val.visit()) + " " 
    return res + ")"





class Binary(Expr):
    def __init__(self, left, right, operator: Token):
        self.left = left
        self.right= right
        self.operator = operator

    def visit(self):
        left = self.left.visit()
        right = self.right.visit()

        match(self.operator.type):

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


class Unary(Expr):
    def __init__(self, operator: Token, expr):
        self.operator: Token = operator
        self.expr = expr 


    def isTrue(self, object):
        if object is not None:
            return bool(object)
        return False


    def visit(self):
        right = None
        if self.expr:
            right = self.expr.visit()
        match(self.operator.type):
            case(TokenType.MINUS):
                if right:
                    return -right
            case(TokenType.BANG):
                if right is not None:
                    return not self.isTrue(right) 
        return None 

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()


class Literal(Expr):
    def __init__(self, val):
        self.value = val

    def visit(self):
        return self.value



