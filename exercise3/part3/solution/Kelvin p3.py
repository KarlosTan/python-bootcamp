from numpy.random import randn
from numpy.random import rand
from numpy.random import seed
import numpy as np
import sympy as sym

seed(1)
experiments = 10
constraint = [-5, 5]
dim1 = 10
dim2 = 20

n_iterations = 1000
step_size = 0.1
temp = 10

#Annealing function
def annealing(self):
        bestx = constraint[0] + rand(self.dim)*(constraint[1]-constraint[0])
        besty = self.eval(bestx)
        currx, curry = bestx, besty
        for i in range(n_iterations):
            testx = currx + randn(self.dim)*step_size
            testy = self.eval(testx)
            if testy < besty:
                bestx, besty = testx, testy
                #print('>%d f(x) = %.5f' % (i, besty))
            diff = testy - curry
            t = temp/float(i+1)
            metropolis = sym.exp(-diff / t)
            if diff < 0 or rand() < metropolis:
                currx, curry = testx, testy
        self.bestx = bestx
        self.besty = besty

#Rosenbrock class
class Rosenbrock:
    def __init__(self, dim):
        self.dim = dim
        self.symb = sym.symbols('x:%d' %self.dim)
        self.a = 1                                  #Parameters
        self.b = 100
        self.fun = 0                                #Define function
        for i in range(self.dim-1):
            self.fun += self.b*(self.symb[i+1] - self.symb[i]**2)**2 + (self.a - self.symb[i])**2
        self.bestx = None                           #Best values stored once found
        self.besty = None
    
    def eval(self, x):
        fun = self.fun
        for i in range(self.dim):
            fun = fun.subs(self.symb[i], x[i])
        return fun.evalf()
    
    def simulated_annealing(self):
        annealing(self)

'''
A = [None]*experiments
for a in range(experiments):
    A[a] = Rosenbrock(dim1)
    A[a].simulated_annealing()

Aresx = np.zeros((experiments, experiments))
Aresy = np.zeros(experiments)
for a in range(len(A)):
    Aresx[a, :] = A[a].bestx
    Aresy[a] = A[a].besty

Ameanx = np.mean(Aresx, axis = 0)
Asdx = np.std(Aresx, axis = 0)
Abest = min(Aresy)

print('Rosenbrock')
print('mean', Ameanx, 'sd', Asdx, 'best', Abest)

mean [-0.00051329  0.22196474  0.12874529  0.08665529  0.04099583  0.00646291  0.00848326 -0.1032491   0.23081547  0.48745975] 
sd [0.47568885 0.28034781 0.23066825 0.17595154 0.08004354 0.02836358 0.03555062 0.38054605 0.63324179 1.41353174] 
best 9.167575839649443
'''


class Rastrigin:
    def __init__(self, dim):
        self.dim = dim
        self.symb = sym.symbols('x:%d' %self.dim)
        self.A = 10
        self.fun = self.A*self.dim
        for i in range(self.dim):
            self.fun += self.symb[i]**2 - self.A*sym.cos(2*sym.pi*self.symb[i])
        self.bestx = None
        self.besty = None

    def eval(self, x):
        fun = self.fun
        for i in range(self.dim):
            fun = fun.subs(self.symb[i], x[i])
        return fun.evalf()

    def simulated_annealing(self):
        annealing(self)

'''
B = [None]*experiments
for b in range(experiments):
    B[b] = Rastrigin(dim1)
    B[b].simulated_annealing()

Bresx = np.zeros((experiments, experiments))
Bresy = np.zeros(experiments)
for b in range(len(B)):
    Bresx[b, :] = B[b].bestx
    Bresy[b] = B[b].besty

Bmeanx = np.mean(Bresx, axis = 0)
Bsdx = np.std(Bresx, axis = 0)
Bbest = min(Bresy)

print('Rastrigin')
print('mean', Bmeanx, 'sd', Bsdx, 'best', Bbest)

mean [ 0.4995365  -0.70362096  0.29084739 -0.40482254  1.00645459 -0.81062064 -0.98514118 -0.59716329  0.47875869 -0.59926904]
sd [2.53712369 3.15500076 2.63534765 1.86088488 3.28555748 2.77539399 2.94896752 3.30307193 2.19293682 2.76109962] 
best 43.865732489311235
'''
class Ellipsoidal:
    def __init__(self, dim):
        self.dim = dim
        self.symb = sym.symbols('x:%d' %self.dim)
        self.fun = 0
        for i in range(1, self.dim+1):
            self.fun += i*self.symb[i-1]**2
        self.bestx = None
        self.besty = None

    def eval(self, x):
        fun = self.fun
        for i in range(self.dim):
            fun = fun.subs(self.symb[i], x[i])
        return fun.evalf()

    def simulated_annealing(self):
        annealing(self)

'''
C = [None]*experiments
for c in range(experiments):
    C[c] = Ellipsoidal(dim1)
    C[c].simulated_annealing()

Cresx = np.zeros((experiments, experiments))
Cresy = np.zeros(experiments)
for c in range(len(C)):
    Cresx[c, :] = C[c].bestx
    Cresy[c] = C[c].besty

Cmeanx = np.mean(Cresx, axis = 0)
Csdx = np.std(Cresx, axis = 0)
Cbest = min(Cresy)

print('Ellipsoidal')
print('mean', Cmeanx, 'sd', Csdx, 'best', Cbest)

mean [-0.0151036  -0.00413657  0.01368213  0.00169114 -0.00827724 -0.00562262 -0.01039326 -0.00951591  0.00329453 -0.00815843]
sd [0.12049213 0.06626607 0.05344578 0.06418886 0.0304028  0.04235599 0.04161411 0.03205038 0.03224345 0.02891074]
best 0.04680342387726258
'''