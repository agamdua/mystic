#!/usr/bin/env python

"""
Example:
    - Solve 8th-order Chebyshev polynomial coefficients with Powell's method.
    - Uses BatchGridSolver to provide 'pseudo-global' optimization
    - Plot of fitting to Chebyshev polynomial.

Demonstrates:
    - standard models
    - minimal solver interface
"""
# the BatchGrid solver
from mystic.nested import BatchGridSolver

# Powell's Directonal solver
from mystic.scipy_optimize import PowellDirectionalSolver

# Chebyshev polynomial and cost function
from mystic.models.poly import chebyshev8, chebyshev8cost
from mystic.models.poly import chebyshev8coeffs

# tools
from mystic.termination import NormalizedChangeOverGeneration as NCOG
from mystic.math import poly1d
from mystic import getch, VerboseSow
import pylab
pylab.ion()

# draw the plot
def plot_exact():
    pylab.title("fitting 8th-order Chebyshev polynomial coefficients")
    pylab.xlabel("x")
    pylab.ylabel("f(x)")
    import numpy
    x = numpy.arange(-1.2, 1.2001, 0.01)
    exact = chebyshev8(x)
    pylab.plot(x,exact,'b-')
    pylab.legend(["Exact"])
    pylab.axis([-1.4,1.4,-2,8],'k-')
    return
 
# plot the polynomial
def plot_solution(params):
    import numpy
    x = numpy.arange(-1.2, 1.2001, 0.01)
    f = poly1d(params)
    y = f(x)
    pylab.plot(x,y,'y-')
    pylab.legend(["Exact","Fitted"])
    pylab.axis([-1.4,1.4,-2,8],'k-')
    return


if __name__ == '__main__':

    print "Powell's Method"
    print "==============="

    # dimensional information
    import random
    random.seed(123)
    ndim = 9
   #nbins = [1]*ndim
    nbins = [2,1,2,1,2,1,1,1,1]

    # draw frame and exact coefficients
    plot_exact()

    # configure monitor
    stepmon = VerboseSow(1)

    # use BatchGrid Powell to solve 8th-order Chebyshev coefficients
    solver = BatchGridSolver(ndim, nbins)
    solver.SetNestedSolver(PowellDirectionalSolver)
   #solver.SetMapper(ez_map)
    solver.SetStrictRanges(min=[-300]*ndim, max=[300]*ndim)
    solver.Solve(chebyshev8cost, NCOG(1e-4), StepMonitor=stepmon, disp=1)
    solution = solver.Solution()

    # use monitor to retrieve results information
    iterations = len(stepmon.x)
    cost = stepmon.y[-1]
    print "Generation %d has best Chi-Squared: %f" % (iterations, cost)

    # use pretty print for polynomials
    print poly1d(solution)

    # compare solution with actual 8th-order Chebyshev coefficients
    print "\nActual Coefficients:\n %s\n" % poly1d(chebyshev8coeffs)

    # plot solution versus exact coefficients
    plot_solution(solution) 
    getch()

# end of file
