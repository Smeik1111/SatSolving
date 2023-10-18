from pysat.solvers import Glucose3
import math
n=15
k_max = 5

number_of_klauses = 0
g = Glucose3()
for i in range(1, n+1): #startbit
    for j in range(1, n+1): #space between triples
        variables = []
        for k in range(0,k_max):
            variables.append(i+k*j)
        if all(x < n+1 for x in variables):
            #print(variables)
            g.add_clause(variables)
            variables_negative = [x*-1 for x in variables]
            g.add_clause(variables_negative)
            number_of_klauses += 2
        
print(g.solve())
print(g.get_model())
print("number of klauses: " + str(number_of_klauses))

#number of Variables = n

#number of klauses with n bits and K amount of numbers in Arhitmetic Progression
# Beginnent bei n==K-1: Bei jedem n % (k-1) == 0 erhöht sich die addierte Zahl um 2
#n  K=3 K=4 K=5
#1  0   0   0
#2  0   0   0
#3  2   0   0
#4  4   2   0
#5  8   4   2
#6  12  6   4
#7  18  10  6
#8  24  14  8
#9  32  18  12
#10 40  24  16
#11 50  30  20
#12 60  36  24
#13 72  44  30 
#14 84  52  36
#15 98  60  42
