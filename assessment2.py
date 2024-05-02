#os imported for clearing the terminal, 
#unittest for validation of correct values in data structures, 
#sys for accessing the testing methods.
import os 
import unittest
import sys

"""
Expression to Binary Tree Parcer


Description:
    This single file program automatically converts mathematical expressions into binary trees and allows for the user to perform operations including a visualised binary tree of an inorder traversal, preorder, postorder, and breadth-first traversals. It also evaluates the expressions based on the constructed tree.

    
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
    No installation required, just run the script with Python installed on your device.

    
Usage:
    Run the script from the command line:
        python assessment2.py

    Read and follow the on-screen menu and prompts to select specific features of this project.
    If you are struggling to see the visualised binary tree or any other wanted outputs, the terminal window may be too small in which you will either need to scroll or expand the window.

Testing:
    To run the tests included with this application, execute the script from your command line with "--test" at the end. For example:
        python assessment2.py --test

    This will initiate the script in test mode, running all predefined unit tests instead of showing the user interface.
    There are 3 main tests used in this code:
            •Tree structure test, used to verify that the bianry tree is constructed correctly for an expression
            •Tree evaluation test, used to check if the tree correctly evauluates an expression to the expected result.
            •Error handling test, used to check if the tree robustly handles errors.
    Once run, it should print something like this:

        ..
        ----------------------------------------------------------------------
        Ran 2 tests in 0.000s
        OK

    The two dots indicate two successful tests have been passed, followed by how many tests and how long it took to execute them.
    'OK' Is then printed to indicate all tests were run without any errors or issues.

    If any issues arise, one of the dots will be replaced with an 'E' or 'F', indicating what test has failed, followed by a traceback showing the exact issue.

    

Credits:
    Binary Tree and traversal information, used as reference: (https://www.geeksforgeeks.org/binary-tree-data-structure/)
    Stacks & Queues Information, used as reference: (https://www.geeksforgeeks.org/stack-and-queues-in-python/)
    Python Documentation, used as reference: (https://docs.python.org/3/)
    Other Python Documentation, used as reference: (https://docs.python-guide.org/writing/documentation/)
    Notes from the CS1527 course were used throughout the implementation and design process.

Information:
    StudentID: 52317470
    Email: u16mm23@abdn.ac.uk

"""


#Class used to represent a node in the binary tree, with value being the value of the node itself and left and right being its children.
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None #Declared as none tather that int or string as unkown whether child will be operator or operand
        self.right = None


#Main function containing interactive loop for inputting the users expressions along with the different options available (visualisation, traversals, calculate, redo equation, exit)
def main():
    while True:
        try:
            clear_screen() #Clearing terminal for declutter
            expression = input("Please enter your expression: ").replace(" ", "")  #Removes any unwanted spaces from the equation before parcing 
            root = parse(expression)
            break  #Ends the loop if parcing was successful 
        except ValueError as e:
            print(f"\nNot a valid expression, {e}")
            response = input("\nPress enter to try again or type 'q' to quit: ")
            if response.lower() == 'q':
                quit()
            

    while True:
        #Dictionary containing number keys pairing to tuples containing both a call to the function and a string to be used in an f-string 
        options = {
            '1': (inorder_visual, "Inorder Traversal"),
            '2': (preorder_traversal, "Preorder Traversal"),
            '3': (postorder_traversal, "Postorder Traversal"),
            '4': (breadth_first_traversal, "Breadth First Traversal"),
            '5': (calculate, "Calculate Result"),
            '6': (main),
            '7': (quit)
        }

        choice = input("Please choose an option from the list below by typing its number: \n"
                       "1. Visualised Inorder Traversal\n"
                       "2. Preorder Traversal\n"
                       "3. Postorder Traversal\n"
                       "4. Breadth First Traversal\n"
                       "5. Calculate Result\n"
                       "6. Change Expression\n"
                       "7. Exit\n: ")

        if choice in options:
            clear_screen()
            if choice == '5':
                result = calculate(root)
                print(f"The calculated result is: {result}")
            elif choice == '6':
                return  # Exits the current main loop and re-invokes it
            elif choice == '7':
                print("Exiting Programme now.")
                break
            else:
                function, description = options[choice]
                print(f"Here is the {description} of your expression:\n")
                function(root)
                print("\n")
        else:
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
    if expression[0] != "(" or expression[-1] != ")":
        raise ValueError("expresisons must be surrounded by opening and closing brackets")
    while i < n:
        character = expression[i]

        #Checking for closing bracket without a matching open.
        if character == ')':
            if not stack or '(' not in stack:
                raise ValueError("brackets mismatched: an extra closing bracket detected.")

            contents = []
            while stack and stack[-1] != '(':
                contents.append(stack.pop())

            if stack[-1] == '(':
                stack.pop() #Checks again for opening bracket, shoud'nt be anything else as that error should be caught at the start of the parsing function, but it is just in case.

            # Check the structure inside the brackets
            if len(contents) != 3 or contents[1] not in '+-*/':
                raise ValueError("each operation must have exactly one operator and two operands.")
            
            # Create a new subtree with left and right children
            right = contents.pop(0)
            operator = contents.pop(0)

             # Check for division by zero during parsing to prevent further issues when calculating
            if operator == '/' and isinstance(right, TreeNode) and right.value == '0':
                raise ValueError("Division by zero is not allowed.")
            
            left = contents.pop(0)
            node = TreeNode(operator)
            node.left = left
            node.right = right
            stack.append(node)

        elif character in '+-*/':
            # Check if an operator is followed by another operator or is at the end
            if i + 1 == n or expression[i+1] in '+-*/':
                raise ValueError(f" invalid sequence of operators near '{character}'.")
            if not stack or not isinstance(stack[-1], TreeNode):
                raise ValueError(f" operator '{character}' is not preceded by an operand.")
            stack.append(character)
        elif character.isdigit():
            # Check if a number is directly followed by another number without an operator
            if stack and isinstance(stack[-1], TreeNode):
                raise ValueError(f" two single digit operands need to have one operator between them - invalid digit:'{character}' .")
            stack.append(TreeNode(character))
        elif character == '(':
            stack.append(character)
        else:
            raise ValueError(f" invalid character in use ({character}), please use only single digits for operands with the operators *, /, +, and -")

        i += 1

    # Final check for unmatched opening brackets
    if len(stack) != 1 or not isinstance(stack[0], TreeNode):
        raise ValueError(" expression is incomplete or brackets are mismatched.")

    return stack[0]  # The root of the constructed binary tree



def inorder_visual(node, indent=""):
    if node is not None:
        # Print the left child with increasing spaces
        inorder_visual(node.left, indent + "   ")

        # Print the current nodes value
        print(f"{indent}{node.value}")

        # Print the right child with increasing spaces
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
    queue = [root]  #uses a list as a queue
    while queue:
        node = queue.pop(0)
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


#Class used for all aspects of testing, divided into seperate functions for specific testing, names are self explanatory.
class TestBinaryTree(unittest.TestCase):
    def test_easy_expression(self):
        expression = "(2/5)"
        root = parse(expression)
        self.assertEqual(root.value, '/')
        self.assertIsInstance(root.left, TreeNode)
        self.assertIsInstance(root.right, TreeNode)
        self.assertEqual(root.left.value, '2')
        self.assertEqual(root.right.value, '5')

    def test_hard_expression(self):
        expression = "((2*3)+(3-4))"
        root = parse(expression)
        self.assertEqual(root.value, '+')
        self.assertIsInstance(root, TreeNode)
        # Check the structure of the left subtree
        self.assertIsInstance(root.left, TreeNode)
        self.assertEqual(root.left.value, '*')
        self.assertIsInstance(root.left.left, TreeNode)
        self.assertEqual(root.left.left.value, '2')
        self.assertIsInstance(root.left.right, TreeNode)
        self.assertEqual(root.left.right.value, '3')
        # Check the structure of the right subtree
        self.assertIsInstance(root.right, TreeNode)
        self.assertEqual(root.right.value, '-')
        self.assertIsInstance(root.right.left, TreeNode)
        self.assertEqual(root.right.left.value, '3')
        self.assertIsInstance(root.right.right, TreeNode)
        self.assertEqual(root.right.right.value, '4')

    #Functions for testing the evaluations of the expressions
    def test_expression_evaluation(self):
        expression = "((2+3)*(4-1))"
        root = parse(expression)
        result = calculate(root)
        self.assertEqual(result, 15)

    #Functions for testing the error handling 
    def test_division_by_zero(self):
        expression = "(1/0)"
        with self.assertRaises(ValueError) as context:
            root = parse(expression)
        self.assertIn("Division by zero is not allowed", str(context.exception))

    def test_mismatched_parentheses(self):
        expressions = "(2+(8*9)"
        with self.assertRaises(ValueError, msg=f"Should handle mismatched parentheses"):
            parse(expressions)

    def test_invalid_characters(self):
        expression = "(2&3)"
        with self.assertRaises(ValueError, msg="Should raise error for invalid characters"):
            parse(expression)


if __name__ == "__main__":
    # Check if "--test" is in the command-line arguments
    if "--test" in sys.argv:
        # Remove "--test" from users text to prevent unittest from processing it and crashing
        sys.argv.remove("--test")
        # Running the unittests
        unittest.main()
    else:
        while True:
            main()
