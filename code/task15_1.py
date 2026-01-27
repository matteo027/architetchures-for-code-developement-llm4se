import re

def evaluate_expression(expr, variables, operators):
    """
    Custom Expression Evaluator with User-Defined Operators

    Evaluate a mathematical expression with custom operators and variables.

    The expression can contain:
    - Integer numbers (positive and negative)
    - Variables (lowercase letters, looked up in the variables dict)
    - Binary operators (defined in operators dict with their precedence and function)
    - Parentheses for grouping

    Args:
        expr: str - the expression to evaluate (e.g., "3 + x * 2")
        variables: dict - maps variable names to their integer values
                         (e.g., {'x': 5, 'y': 10})
        operators: dict - maps operator symbols to (precedence, function) tuples
                         Higher precedence = evaluated first
                         function takes two integers and returns an integer
                         (e.g., {'+': (1, lambda a,b: a+b), '*': (2, lambda a,b: a*b)})

    Returns:
        int - the result of evaluating the expression

    Operator Precedence Rules:
    - Higher precedence operators are evaluated before lower precedence
    - Operators with equal precedence are evaluated left-to-right
    - Parentheses override precedence

    Example 1:
        expr = "3 + 4 * 2"
        variables = {}
        operators = {
            '+': (1, lambda a, b: a + b),
            '*': (2, lambda a, b: a * b)
        }
        Result: 11  (because * has higher precedence: 3 + (4*2) = 3 + 8 = 11)

    Example 2:
        expr = "(3 + 4) * 2"
        variables = {}
        operators = {'+': (1, lambda a,b: a+b), '*': (2, lambda a,b: a*b)}
        Result: 14  (parentheses override: (3+4) * 2 = 7 * 2 = 14)

    Example 3:
        expr = "x + y * 2"
        variables = {'x': 10, 'y': 5}
        operators = {'+': (1, lambda a,b: a+b), '*': (2, lambda a,b: a*b)}
        Result: 20  (10 + (5*2) = 10 + 10 = 20)

    Example 4:
        expr = "10 - 3 - 2"
        variables = {}
        operators = {'-': (1, lambda a,b: a-b)}
        Result: 5  (left-to-right: (10-3) - 2 = 7 - 2 = 5)

    Example 5 (custom operator):
        expr = "2 ^ 3 ^ 2"
        variables = {}
        operators = {'^': (3, lambda a,b: a**b)}  # exponentiation
        Result: 64  (left-to-right: (2^3)^2 = 8^2 = 64)

    Example 6:
        expr = "a @ b + c"
        variables = {'a': 6, 'b': 2, 'c': 5}
        operators = {
            '@': (2, lambda a,b: a // b),  # integer division, higher precedence
            '+': (1, lambda a,b: a + b)
        }
        Result: 8  ((6 // 2) + 5 = 3 + 5 = 8)

    Notes:
    - Whitespace in expressions should be ignored
    - Variable names are single lowercase letters (a-z)
    - Operator symbols can be any non-alphanumeric, non-parenthesis character
    - All arithmetic is integer arithmetic
    - You can assume the expression is valid (balanced parentheses, defined vars)
    """
    tokens = re.findall(r"(\d+|[a-z]|\(|\)|\S)", expr.replace(" ", ""))
    output_queue = []
    operator_stack = []

    def get_precedence(op):
        return operators.get(op, (0, None))[0]

    def is_operator(token):
        return token in operators

    def is_left_associative(op):
        return True # All operators are left-associative in this problem

    for token in tokens:
        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            output_queue.append(int(token))
        elif 'a' <= token <= 'z':
            output_queue.append(variables.get(token, 0))
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  # Pop '('
        elif is_operator(token):
            while (operator_stack and
                   operator_stack[-1] != '(' and
                   (get_precedence(operator_stack[-1]) > get_precedence(token) or
                    (get_precedence(operator_stack[-1]) == get_precedence(token) and is_left_associative(token)))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    evaluation_stack = []
    for token in output_queue:
        if isinstance(token, int):
            evaluation_stack.append(token)
        elif is_operator(token):
            right_operand = evaluation_stack.pop()
            left_operand = evaluation_stack.pop()
            _, func = operators[token]
            result = func(left_operand, right_operand)
            evaluation_stack.append(result)

    return evaluation_stack[0]
