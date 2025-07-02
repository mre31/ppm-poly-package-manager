"""
    Plugin Name: Calculator
    Description: An advanced calculator plugin for Poly.
    Author: mre31
    Version: 2.0
    Last Updated: July 2, 2025

    This plugin is free software and may be copied and used in any way.
"""

import math
import re

# This dictionary now holds all functions and constants available to the user.
# It's the single source of truth for what's allowed in calculations.
SAFE_DICT = {
    # Constants
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,

    # Basic Functions
    "abs": abs,
    "pow": pow,
    "round": round,
    "sqrt": math.sqrt,

    # Trigonometric Functions
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,

    # Hyperbolic Functions
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,

    # Logarithmic & Power Functions
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,

    # Rounding
    "ceil": math.ceil,
    "floor": math.floor,

    # Angle Conversion
    "degrees": math.degrees,
    "radians": math.radians,

    # Other
    "factorial": math.factorial,
    "gamma": math.gamma,
}

def calculate(expression):
    """
    A safe, advanced calculator function that evaluates mathematical expressions.
    Returns a tuple: (result, error_message).
    """
    # Allow only a safe subset of characters. This is a first line of defense.
    allowed_chars = r"^[a-zA-Z0-9\.\+\-\*\/\(\)\s\^,]+$"
    # Replace user-friendly power operator '^' with Python's '**'
    expression = expression.replace('^', '**')

    if not re.match(allowed_chars, expression.replace('**', '')):
        return None, "Error: Invalid characters in expression."

    try:
        # The environment for eval is restricted to our SAFE_DICT.
        # The "__builtins__": {} part is crucial for security, blocking access to Python's built-in functions.
        result = eval(expression, {"__builtins__": {}}, SAFE_DICT)
        return result, None
    except ZeroDivisionError:
        return None, "Error: Division by zero."
    except NameError as e:
        return None, f"Error: Unsupported function or constant used. {e}"
    except Exception as e:
        return None, f"Error: {e}"

def show_help(tab):
    """Displays a formatted help message with all available functions and constants."""
    tab.add("--- Calculator Help ---")
    tab.add("Usage: calc <expression>  OR  = <expression>")
    tab.add("Example: calc sqrt(9) * (pi / 2)")
    tab.add("\nAvailable Operators: +, -, *, /, ** (power), ^ (power)")
    
    # Format functions and constants for display
    constants = sorted([k for k, v in SAFE_DICT.items() if isinstance(v, (int, float))])
    functions = sorted([k for k, v in SAFE_DICT.items() if not isinstance(v, (int, float))])

    tab.add("\nConstants:")
    tab.add("  " + ", ".join(constants))
    
    tab.add("\nFunctions:")
    # Display functions in columns for readability
    col_width = 12
    cols = 4
    func_lines = []
    for i in range(0, len(functions), cols):
        line = "".join(f"{f:<{col_width}}" for f in functions[i:i+cols])
        func_lines.append("  " + line)
    tab.add("\n".join(func_lines))
    tab.add("-----------------------")


def register_plugin(app_context):
    """
    Registers the 'calc' and '=' commands.
    """
    define_command = app_context["define_command"]

    def calc_command(tab, args):
        # Handle the new 'help' command
        if not args or args.strip().lower() == 'help':
            show_help(tab)
            return
        
        result, error = calculate(args)
        if error:
            tab.add(error)
        else:
            tab.add(str(result))

    # Register the main 'calc' command
    define_command("calc", calc_command, "Calculates an advanced mathematical expression.")
    
    # Register the '=' command to use the same function
    define_command("=", calc_command, "Shortcut for the calc command.")
