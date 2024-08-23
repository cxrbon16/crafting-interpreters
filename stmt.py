import interpreter


class Stmt():
    def __init__(self):
        pass

class printStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        interpreter.eval_printStmt(self)


    
class exprStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self):
        interpreter.eval_exprStmt(self)


class varStmt():
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self):
        interpreter.eval_varStmt(self) 
