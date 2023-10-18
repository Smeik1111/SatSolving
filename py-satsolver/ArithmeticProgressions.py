from pysat.solvers import Glucose3
import math
n=9
g = Glucose3()
for i in range(1, n): #startbit
    for j in range(1, n): #space between triples
        a,b,c = i+0*j, i+1*j, i+2*j
        if b <= n and c <= n:
            #print(a,b,c)
            g.add_clause([a, b, c])
            g.add_clause([-a, -b, -c])
print(g.solve())
print(g.get_model())