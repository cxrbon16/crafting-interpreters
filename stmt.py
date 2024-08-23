class Stmt():
    def __init__(self):
        pass

class printStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        val = self.expression.visit()
        print(val)



    
class exprStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        val = self.expression.visit()
        return val



class Var():
    def __init__(self, name, val):
        self.name = name
        self.val = val
    def evaluate():
        
