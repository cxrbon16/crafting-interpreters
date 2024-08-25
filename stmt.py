class Stmt():
    def __init__(self):
        pass

class printStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self, interpreterC):
        interpreterC.eval_printStmt(self)

class blockStmt():
    def __init__(self, stmts) -> None:
        self.statements = stmts
   

    def evaluate(self, interpreterC):
        return interpreterC.eval_blockStmt(self)
class exprStmt():
    def __init__(self, expression):
        self.expression = expression 

    def evaluate(self, interpreterC):
        interpreterC.eval_exprStmt(self)


class varStmt():
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self, interpreterC):
        interpreterC.eval_varStmt(self) 
