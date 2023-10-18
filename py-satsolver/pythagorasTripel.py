from pysat.solvers import Glucose3
import math
n=1000
g = Glucose3()
for i in range(1, n):
    for j in range(1, n):
        k = math.sqrt(i*i + j*j)
        if  k <= n and k.is_integer():
            i,j,k = int(i), int(j), int(k)
            #print(i,j,k)
            g.add_clause([i, j, k])
            g.add_clause([-i, -j, -k])
print(g.solve())
print(g.get_model())