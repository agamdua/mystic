from mystic.symbolic import *
from mystic.math import almostEqual
from mystic.constraints import as_constraint

def test_generate_penalty():

  constraints = """
  x0**2 = 2.5*x3 - a
  exp(x2/x0) >= b"""

  ineq,eq = generate_conditions(constraints, nvars=4, locals={'a':5.0, 'b':7.0})
  assert ineq[0]([4,0,0,1,0]) == 6.0
  assert eq[0]([4,0,0,1,0]) == 18.5

  penalty = generate_penalty((ineq,eq))
  assert penalty([1,0,2,2.4]) == 0.0
  assert penalty([1,0,0,2.4]) == 7200.0
  assert penalty([1,0,2,2.8]) == 100.0

  constraint = as_constraint(penalty, nvars=4, solver='fmin')
  assert almostEqual(penalty(constraint([1,0,0,2.4])), 0.0, 1e-10)

def test_numpy_penalty():

  constraints = """
  mean([x0, x1, x2]) = 5.0
  x0 = x1 + x2"""

  ineq,eq = generate_conditions(constraints)
  assert eq[0]([7,5,3]) == 0.0
  assert eq[1]([7,4,3]) == 0.0

  penalty = generate_penalty((ineq,eq))
  assert penalty([9.0,5,4.0]) == 100.0
  assert penalty([7.5,4,3.5]) == 0.0

  constraint = as_constraint(penalty, solver='fmin')
  assert almostEqual(penalty(constraint([3,4,5])), 0.0, 1e-10)

def test_generate_constraint():

  constraints = """
  mean([x0, x1, x2]) = 5.0
  spread([x0, x1, x2]) = 10.0"""

  from mystic.math.measures import mean, spread
  solv = generate_solvers(constraints)
  assert almostEqual(mean(solv[0]([1,2,3])), 5.0)
  assert almostEqual(spread(solv[1]([1,2,3])), 10.0)

  constraint = generate_constraint(solv)
  assert almostEqual(constraint([1,2,3]), [0.0,5.0,10.0], 1e-10)

def test_solve_constraint():

  constraints = """
  spread([x0,x1]) - 1.0 = mean([x0,x1])   
  mean([x0,x1,x2]) = x2"""

  from mystic.math.measures import mean, spread
  _constraints = solve(constraints)
  solv = generate_solvers(_constraints)
  constraint = generate_constraint(solv)
  x = constraint([1.0, 2.0, 3.0])
  assert all(x) == all([1.0, 5.0, 3.0])
  assert mean(x) == x[2]
  assert spread(x[:-1]) - 1.0 == mean(x[:-1])


if __name__ == '__main__':
  test_generate_penalty()
  test_numpy_penalty()
  test_generate_constraint()
  test_solve_constraint()

