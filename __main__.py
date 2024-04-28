class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse_expression(expression):
    stack = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char == ' ':
            i += 1
            continue

        if char == '(':
            # Simply push the '(' onto stack to denote an expression start
            stack.append(char)
        elif char.isdigit():
            # Create a tree node for the digit and push it onto the stack
            stack.append(TreeNode(char))
        elif char in '+-*/':
            # Push the operator onto the stack
            stack.append(char)
        elif char == ')':
            # Upon encountering a ')', start popping from the stack until '('
            if len(stack) < 4:  # There should be at least one operator and two operands
                raise ValueError("Malformed expression: insufficient operands or operators before ')'.")
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()

            # Ensure that the operands and operator are correctly placed
            if isinstance(left, str) or isinstance(right, TreeNode) and isinstance(left, TreeNode):
                raise ValueError("Malformed expression: incorrect placement of operators and operands.")

            if stack.pop() != '(':  # This should be the matching '('
                raise ValueError("Malformed expression: no matching '(' found for ')'.")

            # Create a new subtree with the operator as the root
            node = TreeNode(operator)
            node.left = left
            node.right = right

            # Push the new subtree back onto the stack
            stack.append(node)
        else:
            raise ValueError(f"Invalid character found in expression: {char}")

        i += 1

    if len(stack) != 1:
        raise ValueError("Malformed expression: unmatched parentheses or incomplete expression.")
    
    return stack[0]  # The root of the constructed binary tree

# Example Usage
expression = "(((2*(3+2))+5)/2)"
try:
    root = parse_expression(expression)
    print(f"Root of the tree is: {root.value} (with left value {root.left.value} and right value {root.right.value})")
except ValueError as e:
    print(e)
