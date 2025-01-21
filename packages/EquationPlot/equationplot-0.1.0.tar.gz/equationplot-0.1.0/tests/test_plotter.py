from equationplot.plotter import solve_equation

def test_solve_equation():
    roots = solve_equation("x**2 - 4")
    assert roots == [-2, 2]
