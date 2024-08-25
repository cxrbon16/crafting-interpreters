class Environment():
    def __init__(self, enclosing):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, val):

        self.values[name] = val
        return self.values
    
    def assign(self, name, val):
        if name in self.values:
            self.values[name] = val
        else:
            if self.enclosing:
                self.enclosing.assign(name, val)
            return 
            raise Exception(f"undefined variable: {name}")


    def get(self, name):
        if name in self.values:
            return self.values[name]
        else:
            if self.enclosing:
                return self.enclosing.get(name)
            else:
                raise Exception(f"undefined variable: {name}")
        
