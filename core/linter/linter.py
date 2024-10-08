import ast
import os, sys

class CodeStyleChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.http_verbs = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head'}

    def visit_FunctionDef(self, node):
        function_name = node.name
        function_line = node.lineno

        # Skip special methods (e.g., __init__, __str__)
        if function_name[:2] == '__' and function_name[-2:] == '__':
            self.generic_visit(node)
            return
        
        # Check if the function has the @api_view decorator
        if any(isinstance(decorator, ast.Call) and
               isinstance(decorator.func, ast.Name) and
               decorator.func.id == 'api_view' for decorator in node.decorator_list):
            function_name = node.name
            # Ensure function name contains an HTTP verb
            if '_' not in function_name:
                self.errors.append(f"Function '{function_name}' on line {node.lineno} must be multi-part like: create_user, get_transactions, get_transaction_detail.")
            if not any(verb in function_name.lower() for verb in self.http_verbs):
                self.errors.append(f"Function '{function_name}' on line {node.lineno} does not include an HTTP verb.")

        self.check_function_name(function_name, function_line)
        self.generic_visit(node)
    
    # Check if the class name follows CamelCase convention
    def visit_ClassDef(self, node):
        class_name = node.name

        if not self.is_camel_case(class_name):
            self.errors.append(
                f"Class '{class_name}' on line {node.lineno} does not follow CamelCase convention."
            )

        self.generic_visit(node)


    def check_function_name(self, function_name, function_line):
        if len(function_name) < 3:
            error_message = {f"Function name '{function_name} on line {function_line} is to short!"}
            self.errors.append(error_message)
        elif not self.is_snake_case(function_name):
            error_message = {f"Function name '{function_name}' on line {function_line} is not in snake_case."}
            self.errors.append(error_message)

    def is_snake_case(self, name):
        return name == name.lower() and "_" in name

    def is_camel_case(self, name):
        return name[0].isupper()

    def lint(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.errors

def lint_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return
    
    with open(filepath, 'r') as file:
        code = file.read()
    
    linter = CodeStyleChecker()
    errors = linter.lint(code)
    
    if not errors:
        print('Everything Is Good!')
        
    for error in errors:
        print(f"{filepath}: {error}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linter.py <file1> <file2> ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        lint_file(filepath)
