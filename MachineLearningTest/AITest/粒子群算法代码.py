import numpy as np
import random
import matplotlib.pyplot as plt


class PSO():

    def __init__(self, pN, dim, max_iter):
        self.w = 0.8
        self.c1 = 2
        self.c2 = 2
        self.r1 = 0.6
        self.r2 = 0.3
        self.pN = pN  
        self.dim = dim  
        self.max_iter = max_iter  
        self.X = np.zeros((self.pN, self.dim)) 
        self.V = np.zeros((self.pN, self.dim))
        self.pbest = np.zeros((self.pN, self.dim)) 
        self.gbest = np.zeros((1, self.dim))
        self.p_fit = np.zeros(self.pN)  
        self.fit = 1e10 


    def function(self, X):
        return X ** 4 - 2 * X + 3


    def init_Population(self):
        for i in range(self.pN):  
            for j in range(self.dim): 
                self.X[i][j] = random.uniform(0, 1)
                self.V[i][j] = random.uniform(0, 1)
            self.pbest[i] = self.X[i]  
            tmp = self.function(self.X[i]) 
            self.p_fit[i] = tmp
            if tmp < self.fit:
                self.fit = tmp
                self.gbest = self.X[i]

    def iterator(self):
        fitness = []
        for t in range(self.max_iter):  
            for i in range(self.pN): 
                temp = self.function(self.X[i])
                if temp < self.p_fit[i]:  
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] < self.fit: 
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                self.X[i] = self.X[i] + self.V[i]
            fitness.append(self.fit)
            print(self.X[0], end=" ")
            print(self.fit)  
        return fitness

my_pso = PSO(pN=30, dim=1, max_iter=100)
my_pso.init_Population()
fitness = my_pso.iterator()

# plt.figure(1)
# plt.title("Figure1")
# plt.xlabel("iterators", size=14)
# plt.ylabel("fitness", size=14)
# t = np.array([t for t in range(0, 100)])
# fitness = np.array(fitness,dtype=object)
# plt.plot(t, fitness, color='b', linewidth=3)
# plt.show()
