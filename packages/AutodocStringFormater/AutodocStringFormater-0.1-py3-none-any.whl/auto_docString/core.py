import ast
import astor

def generate_docstring(node):
    """
    Generate a docstring for a given AST node (function, class, or method).
    """
    docstring = f'"""\n{node.name}\n\n'

    if isinstance(node, ast.FunctionDef):
        docstring += "Args:\n"
        for arg in node.args.args:
            docstring += f"    {arg.arg}: Description of {arg.arg}\n"

        if node.returns:
            docstring += f"Returns:\n    Description of return value\n"

    docstring += '"""'
    return docstring

def add_docstrings(tree):
    """
    Add docstrings to functions, classes, and methods in the AST.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if not ast.get_docstring(node):
                # Add a docstring if one doesn't exist
                docstring = generate_docstring(node)
                docstring_node = ast.Expr(value=ast.Str(s=docstring))
                node.body.insert(0, docstring_node)

def auto_docString(file_path):
    """
    Automatically add docstrings to a Python file and save it as a new file.
    """
    # Parse the code
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)

    # Add docstrings
    add_docstrings(tree)

    # Generate the updated code
    updated_code = astor.to_source(tree)

    # Save the updated code to a new file
    new_file_path = file_path.replace(".py", "_with_docstrings.py")
    with open(new_file_path, "w") as file:
        file.write(updated_code)

    print(f"Docstrings added. New file saved as: {new_file_path}")