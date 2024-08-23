class Environment():
    def __init__(self):
        self.values = {}

    def define(self, name, val):

        if name in self.values:
            self.values[name] = val

        else:
            self.values.update({name: val})

        return self.values


    def get(self, name):
        if name in self.values:
            return self.values[name]
        else:
            raise Exception(f"undefined variable: {name}")
        
