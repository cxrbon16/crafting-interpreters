import interpreter


class Stmt():
    def __init__(self):
        pass

class printStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        interpreter.eval_printStmt(self.expression)


    
class exprStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        interpreter.eval_exprStmt(self.expression)


class varStmt():
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def evaluate(self):
        interpreter.eval_varStmt(self.name, self.val) 
