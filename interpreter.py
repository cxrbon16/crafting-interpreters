class Interpreter():
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
       
    def interpret(self):
        for stmt in self.stmt_list:
            stmt.evaluate()
