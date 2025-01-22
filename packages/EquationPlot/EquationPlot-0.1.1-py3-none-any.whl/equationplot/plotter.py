import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_function(equation, x_range=(-10, 10), y_range=None):
    """
    Plot a given mathematical function with user-defined ranges.
    
    Args:
        equation (str): The equation as a string (e.g., "x**2 + 2*x - 3").
        x_range (tuple): The range of x-values to plot (default: -10 to 10).
        y_range (tuple, optional): The range of y-values for the plot. If None, it is auto-determined.
    """
    x = sp.symbols('x')
    expr = sp.sympify(equation)

    # Generate x and y values
    x_vals = np.linspace(x_range[0], x_range[1], 500)
    y_vals = [sp.lambdify(x, expr, 'numpy')(val) for val in x_vals]

    # Plot the function
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=f"y = {equation}")

    # Axes and ranges
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    if y_range:
        plt.ylim(y_range)  # Set custom y-range if provided
    plt.grid(alpha=0.3)

    # Annotations
    plt.legend()
    plt.title("Equation Plot")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def solve_equation(equation):
    """
    Solve a given equation for its roots.
    
    Args:
        equation (str): The equation as a string (e.g., "x**2 - 4").
    
    Returns:
        list: The roots of the equation.
    """
    x = sp.symbols('x')
    expr = sp.sympify(equation)
    roots = sp.solve(expr, x)
    return roots
