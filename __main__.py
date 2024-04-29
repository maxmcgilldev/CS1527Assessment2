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
                '5': (main, "Change expression"),
                '6': (quit, "Exit") 
            }

            choice = input("\nPlease choose an option from the list below by typing its number: \n"
                            "1. Visualised Inorder Traversal\n"
                            "2. Preorder Traversal\n"
                            "3. Postorder Traversal\n"
                            "4. Breadth First Traversal\n"
                            "5. Change expression\n"
                            "6. Exit\n\n: ") 
            if choice == "5":
                clear_screen()
                main()

            if choice == "6":
                clear_screen()
                print("Exiting Programme now.")
                options[choice][0]()  # Call the function directly
                break  # Ensure we break after quitting to avoid further execution

            elif choice in options:
                clear_screen() 
                print(f"Here is the {options[choice][1]} of your expression:\n")
                options[choice][0](root)  # Call the function directly using options[choice][0]
                print("\n")
                
            else:
                clear_screen()
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
            stack.append(character)
        elif character.isdigit():
            stack.append(TreeNode(character))
        elif character in '+-*/': 
            stack.append(character)
        elif character == ')':
            if not stack or '(' not in stack:
                raise ValueError("Not a valid expression, brackets mismatched: an extra closing bracket detected.")
            
            contents = []
            while stack and stack[-1] != '(':
                contents.append(stack.pop())

            if stack[-1] == '(':
                stack.pop()
            else:
                raise ValueError("Not a valid expression, brackets mismatched: no matching opening bracket.")

            if len(contents) != 3 or contents[1] not in '+-*/':
                raise ValueError("Not a valid expression, each operator must be flanked by exactly two operands.")


            # Assuming valid format [operand, operator, operand]
            right = contents.pop(0)
            operator = contents.pop(0)
            left = contents.pop(0)

            # Create a new subtree
            node = TreeNode(operator)
            node.left = left
            node.right = right
            stack.append(node)
        else:
            raise ValueError(f"Not a valid expression, invalid character in use ({character}), please stick to single digits for operands with the operators *,/,+ and -")

        i += 1

    if len(stack) != 1 or isinstance(stack[0], str):
        raise ValueError("Not a valid expression, expression is incomplete or brackets are mismatched.")

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
