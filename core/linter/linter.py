import ast

class FunctionNameLinter(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node):
        function_name = node.name

        if not self.is_snake_case(function_name):
            self.errors.append(f"Function name '{function_name}' on line {node.lineno} is not in snake_case.")
        # This calls the generic visit method to continue visiting other nodes
        self.generic_visit(node)

    def is_snake_case(self, name):
        return name == name.lower() and "_" in name

    def lint(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.errors

def lint_file(filepath):
    with open(filepath, 'r') as file:
        code = file.read()
    
    linter = FunctionNameLinter()
    errors = linter.lint(code)
    
    if errors.__len__() == 0:
        print('Everything Is Good!')
        
    for error in errors:
        print(f"{filepath}: {error}")

if __name__ == "__main__":
    filepath = ''
    lint_file(filepath)
