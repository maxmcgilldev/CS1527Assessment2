class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse(expression):
    stack = []
    i = 0
    n = len(expression)

    while i < n:
        character = expression[i]

        if character == '(':
            # Simply push the '(' onto stack to denote an expression start
            stack.append(character)
        elif character.isdigit():
            # Create a tree node for the digit and push it onto the stack
            stack.append(TreeNode(character))
        elif character in '+-*/': 
            # Push the operator onto the stack
            stack.append(character)
        elif character == ')':
            # Upon encountering a ')', start popping from the stack until '('
            if len(stack) < 4:  # There should be at least one operator and two operands
                raise ValueError("Malformed expression: insufficient operands or operators before ')'.")
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()
            print(f"Left: {left.value}, Operator: {operator}, Right: {right.value}")

            # Ensure that the operands and operator are correctly placed
            if not (isinstance(left, TreeNode) and isinstance(right, TreeNode) and isinstance(operator, str)):
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
            raise ValueError(f"Invalid character found in expression: {character}")

        i += 1

    if len(stack) != 1:
        raise ValueError("Malformed expression: unmatched parentheses or incomplete expression.")
    
    return stack[0]  # The root of the constructed binary tree
    




def print_in_order_visual(node, indent="", last="updown"):
    if node is not None:
        # Print the left child, passing down the indentation
        print_in_order_visual(node.left, indent + "     ", "up")

        # Print the current node's value
        if last == "up":
            print(f"{indent}    /-- {node.value}")
        elif last == "down":
            print(f"{indent}    \\-- {node.value}")
        else:
            print(f"{indent}    {node.value}")

        # Print the right child
        print_in_order_visual(node.right, indent + "     ", "down")









def print_tree(node, level=0, prefix="Root: "):
    if node is None:
        return  # Simply return without printing anything if the node is None

    # Print the current node with its level indentation
    print(' ' * (level * 4) + prefix + str(node.value))
    
    # Recursively print left and right children, adding indentation
    print_tree(node.left, level + 1, "L--- ")
    print_tree(node.right, level + 1, "R--- ")




def preorder_traversal(node):
    if node is not None:
        print(node.value, end=' ')
        preorder_traversal(node.left)
        preorder_traversal(node.right)

def postorder_traversal(node):
    if node is not None:
        postorder_traversal(node.left)
        postorder_traversal(node.right)
        print(node.value, end=' ')

def breadth_first_traversal(root):
    if root is None:
        return
    
    queue = [root]  # Use a list as a queue
    while queue:
        node = queue.pop(0)  # Pop the first element; note this is O(n) operation
        print(node.value, end=' ')
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)





# Example Usage
expression = "(((2*(3-2))+6)/3)"
try:
    root = parse(expression)
    print(f"Root of the tree is: {root.value} (with left value {root.left.value} and right value {root.right.value})")
    print_tree(root)
    preorder_traversal(root)
    print("\n")
    postorder_traversal(root)
    print("\n")
    breadth_first_traversal(root)

except ValueError as e:
    print(e)

