class Node:
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.variables = []
        self.functions = []
        self.color = None

    def add_variable(self, variable):
        self.variables.append(variable)

    def add_function(self, function):
        self.functions.append(function)

    def to_graphviz(self):
        var_section = "\\n".join(self.variables).replace("<", "\\<").replace(">", "\\>") if self.variables else "(None)"
        func_section = "\\n".join(self.functions).replace("<", "\\<").replace(">", "\\>") if self.functions else "(None)"
        return f"{{ {self.name} [{self.key}] | {{ Variables:\\n|{var_section} }} | {{ Functions:\\n|{func_section} }} }}"
