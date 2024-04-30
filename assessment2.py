#importing os library in order to clear the users terminal depending on which system they are using.
import os 

"""
Expression to Binary Tree Parcer

Description:
    This single file program automatically converts mathematical expressions into binary trees and allows for the user to perform operations such as
    inorder, preorder, postorder, and breadth-first traversals. It also evaluates the expressions based on the constructed tree.

Features:
    • Automatically parses mathematical expressions into binary trees.
    • Can Visually Output the Binary tree using an inorder traversal (reads right to left when tilted 90° right).
    • Options for variety of traversal methods (sequence printed in terminal):
        • Preorder traversal
        • Postorder traversal
        • Breadth-Frist Traversal
    • Can evaluate expressions - calculates and outputs the tree structured expression to the terminal.
    • Error Handling: error reporting for included for input errors such as mismatched parentheses, invalid characters, missing opening/closing parentheses and wrongly formatted expressions.
    • User-Friendly Interface: Added an interactive terminal user interface to guide the user through the different features and options available to them.

Installation:
    No installation required, just run the script with Python 3.8 or higher.

Usage:
    Run the script from the command line:
        python assessment2.py

    Read and follow the on-screen menu and prompts to select specific features of this project.

Testing:

Credits:
    Binary Tree and traversal information, used as reference (https://www.geeksforgeeks.org/binary-tree-data-structure/)
    Stacks & Queues Information, used as reference (https://www.geeksforgeeks.org/stack-and-queues-in-python/)
    Python Documentation, used as reference(https://docs.python.org/3/)
    Other Python Documentation, used as reference (https://docs.python-guide.org/writing/documentation/)


Information:
    StudentID: 52317470
    Email: u16mm23@abdn.ac.uk

"""


#Class used to represent a node in the binary tree, with value being the value of the node itself and left and right being its children.
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


#Main function containing interactive loop for inputting the users expressions along with the different options available (visualisation, traversals, calculate, redo equation, exit)
def main():
    while True:
        try:
            clear_screen()
            expression = input("Please enter your expression: ").replace(" ", "")  #Removes any unwanted spaces from the equation before parcing 
            root = parse(expression)
            break  #Ends the loop if parcing was successful 
        except ValueError as e:
            print(f"\nError: {e}")
            response = input("\nPress enter to try again or type 'q' to quit: ")
            if response.lower() == 'q':
                quit()
            

    while True:
        options = {
            '1': (inorder_visual, "Inorder Traversal"),
            '2': (preorder_traversal, "Preorder Traversal"),
            '3': (postorder_traversal, "Postorder Traversal"),
            '4': (breadth_first_traversal, "Breadth First Traversal"),
            '5': (calculate, "Calculate Result"),
            '6': (main, "Change expression"),
            '7': (quit, "Exit")
        }

        choice = input("\nPlease choose an option from the list below by typing its number: \n"
                       "1. Visualised Inorder Traversal\n"
                       "2. Preorder Traversal\n"
                       "3. Postorder Traversal\n"
                       "4. Breadth First Traversal\n"
                       "5. Calculate Result\n"
                       "6. Change Expression\n"
                       "7. Exit\n: ")

        if choice == '6':
            main()
        elif choice == '7':
            clear_screen()
            print("Exiting Programme now.")
            break  # Correct exit from the loop
        elif choice in options:
            clear_screen()
            if choice == '5':
                result = calculate(root)
                print(f"The calculated result is: {result}")
            else:
                print(f"Here is the {options[choice][1]} of your expression:\n")
                options[choice][0](root)
                print("\n")
        else:
            clear_screen()
            print("Invalid option, please choose a valid number from the menu")


#Function used for clearing terminal to reduce clutter making it easier for user to understand
def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  #If not windows (mac,linux).
        os.system('clear')

#Parses users math expression and constructs the binary tree from it, also deals with and raises any errors in the format of the expression.
def parse(expression):  
    stack = []
    i = 0
    n = len(expression)

    while i < n:
        character = expression[i]

        #Checking for closing bracket without a matching open.
        if character == ')':
            if not stack or '(' not in stack:
                raise ValueError("Not a valid expression, brackets mismatched: an extra closing bracket detected.")

            contents = []
            while stack and stack[-1] != '(':
                contents.append(stack.pop())

            if stack[-1] == '(':
                stack.pop()
            else:
                raise ValueError("Not a valid expression, brackets mismatched: no matching opening bracket.")

            # Check the structure inside the brackets
            if len(contents) != 3 or contents[1] not in '+-*/':
                raise ValueError("Not a valid expression, each operation must have exactly one operator and two operands.")

            # Create a new subtree with left and right children
            right = contents.pop(0)
            operator = contents.pop(0)
            left = contents.pop(0)
            node = TreeNode(operator)
            node.left = left
            node.right = right
            stack.append(node)
        elif character in '+-*/':
            # Check if an operator is followed by another operator or is at the end
            if i + 1 == n or expression[i+1] in '+-*/':
                raise ValueError(f"Not a valid expression, invalid sequence of operators near '{character}'.")
            if not stack or not isinstance(stack[-1], TreeNode):
                raise ValueError(f"Not a valid expression, operator '{character}' is not preceded by an operand.")
            stack.append(character)
        elif character.isdigit():
            # Check if a number is directly followed by another number without an operator
            if stack and isinstance(stack[-1], TreeNode):
                raise ValueError(f"Not a valid expression, two single digit operands need to have one operator between them - invalid digit:'{character}' .")
            stack.append(TreeNode(character))
        elif character == '(':
            stack.append(character)
        else:
            raise ValueError(f"Not a valid expression, invalid character in use ({character}), please use only single digits for operands with the operators *, /, +, and -")

        i += 1

    # Final check for unmatched opening brackets
    if len(stack) != 1 or not isinstance(stack[0], TreeNode):
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


def calculate(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return int(node.value)
    left_val = calculate(node.left)
    right_val = calculate(node.right)
    if node.value == '+':
        return left_val + right_val
    elif node.value == '-':
        return left_val - right_val
    elif node.value == '*':
        return left_val * right_val
    elif node.value == '/':
        if right_val == 0:
            raise ValueError("Division error, cannot divide by zero.")
        return left_val / right_val  # Ensure division returns a result
    

if __name__ == "__main__":
    main()
