import os


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def main():
    try:
        clear_screen() 
        expression = input("Please enter your expression: ").replace(" ", "")  # Remove spaces
        root = parse(expression)
        while True:
            options = {
                '1': (inorder_visual, "Inorder Traversal"),
                '2': (preorder_traversal, "Preorder Traversal"),
                '3': (postorder_traversal, "Postorder Traversal"),
                '4': (breadth_first_traversal, "Breadth First Traversal"),
                '5': (quit, "Exit") 
            }

            choice = input("\nPlease choose an option from the list below by typing its number: \n"
                            "1. Visualised Inorder Traversal\n"
                            "2. Preorder Traversal\n"
                            "3. Postorder Traversal\n"
                            "4. Breadth First Traversal\n"
                            "5. Exit\n\n: ") 
                       
            if choice == "5":
                clear_screen()
                print("Exiting Programme now.")
                options[choice][0]()  # Call the function directly
                break  # Ensure we break after quitting to avoid further execution
            elif choice in options:
                clear_screen() 
                print(f"Here is the {options[choice][1]} of your equation:\n")
                options[choice][0](root)  # Call the function directly using options[choice][0]
                print("\n")
            else:
                print("Invalid option, please choose a valid number from the menu")
          
    except ValueError as e:
        print(e)


def clear_screen():
    # Clear the command line screen.
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for macOS and Linux
        os.system('clear')


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
            if len(stack) < 4:  # There should be one operator and two operands
                raise ValueError("not a vaid expression, there should be at least one operator and two operands between brackets')'.")
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()

            # Ensure that the operands and operator are correctly placed
            if not (isinstance(left, TreeNode) and isinstance(right, TreeNode) and isinstance(operator, str)):
                raise ValueError("not a valid expression, operators and operands are misplaced")

            if stack.pop() != '(':  # This should be the matching '('
                raise ValueError("not a valid expression, there are an uneven amount of opening parentheses")

            # Create a new subtree with the operator as the root
            node = TreeNode(operator)
            node.left = left
            node.right = right

            # Push the new subtree back onto the stack
            stack.append(node)
        else:
            raise ValueError(f"not a valid expression, invalid character in use: {character}")

        i += 1

    if len(stack) != 1:
        raise ValueError("not a valid expression, there may be unmatched parentheses or it is incomplete")
    
    return stack[0]  # The root of the constructed binary tree


def inorder_visual(node, indent=""):
    if node is not None:
        # Print the left child, increasing indentation
        inorder_visual(node.left, indent + "   ")

        # Print the current node's value
        print(f"{indent}{node.value}")

        # Print the right child, increasing indentation
        inorder_visual(node.right, indent + "   ")


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


if __name__ == "__main__":
    main()
