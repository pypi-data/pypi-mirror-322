import ast
import json
import re
import os
import sys
from typing import Any

class KeywordTranslator(ast.NodeTransformer):
    def __init__(self, language_map):
        self.language_map = language_map

    def translate_keyword(self, value):
        """Translate a single keyword if it's in the language map."""
        return self.language_map.get(value, value)

    def visit_Name(self, node: ast.Name) -> Any:
        """Translate variable and function names if they match a keyword."""
        if node.id in self.language_map:
            return ast.copy_location(ast.Name(id=self.translate_keyword(node.id), ctx=node.ctx), node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """Translate function names and their arguments."""
        node.name = self.translate_keyword(node.name)
        node.args.args = [ast.copy_location(ast.arg(arg=self.translate_keyword(arg.arg), annotation=arg.annotation), arg)
                          for arg in node.args.args]
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg) -> Any:
        """Translate function argument names."""
        node.arg = self.translate_keyword(node.arg)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """Translate attributes if they match a keyword."""
        node.attr = self.translate_keyword(node.attr)
        return self.generic_visit(node)

    def visit_Str(self, node: ast.Str) -> Any:
        """Ensure strings are not translated."""
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        """Translate function calls."""
        node.func = self.visit(node.func)
        node.args = [self.visit(arg) for arg in node.args]
        node.keywords = [self.visit(kw) for kw in node.keywords]
        return node

    def visit_For(self, node: ast.For) -> Any:
        """Translate for-loops with proper context."""
        node.target = self.visit(node.target)
        node.iter = self.visit(node.iter)
        node.body = [self.visit(stmt) for stmt in node.body]
        node.orelse = [self.visit(stmt) for stmt in node.orelse]
        return node

class PreProcessor:
    def __init__(self, language_file):
        self.language_map = self.load_language_map(language_file)

    def load_language_map(self, language_file):
        """Load the keyword mapping for the target language."""
        try:
            with open(language_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Language file '{language_file}' not found.")

    def extract_and_replace_strings(self, code):
        """Extract string literals and replace them with placeholders."""
        string_pattern = r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|\'[^\']*\'|"[^"]*")'
        self.strings = re.findall(string_pattern, code)
        for i, string in enumerate(self.strings):
            placeholder = f"__STRING_PLACEHOLDER_{i}__"
            code = code.replace(string, placeholder, 1)
        return code

    def restore_strings(self, code):
        """Restore string literals from placeholders."""
        for i, string in enumerate(self.strings):
            placeholder = f"__STRING_PLACEHOLDER_{i}__"
            code = code.replace(placeholder, string, 1)
        return code

    def pre_translate_keywords(self, code):
        """Perform raw keyword-based translation before parsing."""
        for hindi, english in self.language_map.items():
            code = code.replace(hindi, english)
        return code

    def translate_code(self, code):
        """Translate the code using pre-translation and AST transformations."""
        # Replace strings with placeholders
        code_without_strings = self.extract_and_replace_strings(code)
        # Perform raw translation for keywords
        code_pre_translated = self.pre_translate_keywords(code_without_strings)
        # Parse the code into an AST and translate further
        tree = ast.parse(code_pre_translated)
        translator = KeywordTranslator(self.language_map)
        translated_tree = translator.visit(tree)
        translated_code = ast.unparse(translated_tree)
        # Restore original strings
        return self.restore_strings(translated_code)

    def translate_file(self, input_file, output_file):
        """Translate an entire file."""
        with open(input_file, 'r', encoding='utf-8') as infile, \
              open(output_file, 'w', encoding='utf-8') as outfile:
            code = infile.read()
            translated_code = self.translate_code(code)
            outfile.write(translated_code)

    def execute_translated_code(self, code):
        """Execute the translated Python code."""
        exec(code, {})

    def execute_file_directly(self, input_file):
        """Translate and execute a file without saving it."""
        with open(input_file, 'r', encoding='utf-8') as infile:
            code = infile.read()
            translated_code = self.translate_code(code)
            self.execute_translated_code(translated_code)

    def translate_directory(self, input_dir, output_dir):
        """Translate all Python files in a directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.py'):
                    input_file = os.path.join(root, file)
                    relative_path = os.path.relpath(input_file, input_dir)
                    output_file = os.path.join(output_dir, relative_path)

                    output_file_dir = os.path.dirname(output_file)
                    if not os.path.exists(output_file_dir):
                        os.makedirs(output_file_dir)

                    self.translate_file(input_file, output_file)
    


    def execute_directory(self, input_dir, main_file):
        """Translate a directory and execute the specified main file."""
        temp_dir = "temp_translated_dir"
        self.translate_directory(input_dir, temp_dir)
    
        # Path to the translated main file in the temporary directory
        translated_main_file_path = os.path.join(temp_dir, main_file)
        if not os.path.exists(translated_main_file_path):
            raise FileNotFoundError(f"Main file '{main_file}' not found in translated directory.")
    
        # Add temp_dir to sys.path so imports from translated modules work
        sys.path.insert(0, temp_dir)
    
        # Execute the translated main file
        with open(translated_main_file_path, 'r', encoding='utf-8') as main_file:
            translated_code = main_file.read()
            print(f"Executing translated main file: {translated_main_file_path}")
            self.execute_translated_code(translated_code)
