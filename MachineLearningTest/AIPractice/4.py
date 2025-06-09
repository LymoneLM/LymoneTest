from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import random

data_path = "./data"
data = loadmat(data_path+'/position.mat')['C'].astype(np.float32)
print(data)
def get_distance (a, b):
    return np.sqrt(np.sum((a - b)**2))

distance = [[get_distance(i, j) for j in data] for i in data]

# 遗传算法参数
NP = 200  # 种群大小
N = 31  # 城市数量
G = 2000  # 最大进化代数
Pc = 0.8  # 交叉概率
Pm = 0.3  # 变异概率


# 计算路径总长度
def calc_path_length(path):
    total_distance = 0
    for i in range(N):
        total_distance += distance[path[i]][path[(i + 1) % N]]
    return total_distance


# 初始化种群
def initialize_population():
    population = []
    for _ in range(NP):
        individual = list(range(N))
        random.shuffle(individual)
        population.append(individual)
    return population


# 选择操作 (轮盘赌选择)
def selection(population, fitness, tournament_size = 5):
    selected = []
    for _ in range(NP):
        # 随机选择 tournament_size 个个体进行比赛
        candidates = random.sample(range(len(population)), tournament_size)
        candidate_fitness = [fitness[i] for i in candidates]
        # 选择适应度最高的
        winner = candidates[np.argmax(candidate_fitness)]
        selected.append(population[winner].copy())
    return selected

# 交叉操作 (部分映射交叉 PMX)
def crossover(parent1, parent2):
    if random.random() > Pc:
        return parent1.copy(), parent2.copy()

    size = len(parent1)
    # 随机选择两个交叉点
    point1 = random.randint(0, size - 2)
    point2 = random.randint(point1 + 1, size - 1)

    # 初始化子代
    child1 = [-1] * size
    child2 = [-1] * size

    # 复制中间段
    for i in range(point1, point2 + 1):
        child1[i] = parent2[i]
        child2[i] = parent1[i]

    # 填充剩余位置
    for i in range(size):
        if i < point1 or i > point2:
            # 子代1
            gene = parent1[i]
            while gene in child1[point1:point2 + 1]:
                idx = parent2.index(gene)
                gene = parent1[idx]
            child1[i] = gene

            # 子代2
            gene = parent2[i]
            while gene in child2[point1:point2 + 1]:
                idx = parent1.index(gene)
                gene = parent2[idx]
            child2[i] = gene

    return child1, child2


# 变异操作 (交换变异)
def mutation(individual):
    if random.random() > Pm:
        return individual

    size = len(individual)
    # 随机选择两个不同的位置
    idx1, idx2 = random.sample(range(size), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


# 主遗传算法
def genetic_algorithm():
    # 初始化种群
    population = initialize_population()
    best_individual = None
    best_fitness = float('inf')
    history = []  # 记录每代最优解

    # 迭代进化
    for generation in range(G):
        # 计算适应度 (路径长度的倒数)
        fitness = [1 / calc_path_length(ind) for ind in population]

        # 更新全局最优解
        for i in range(NP):
            current_length = 1 / fitness[i]
            if current_length < best_fitness:
                best_fitness = current_length
                best_individual = population[i].copy()

        history.append(best_fitness)
        if generation % 100 == 0:
            print(f"Generation {generation}: Best Length = {best_fitness:.4f}")

        # 选择操作
        selected_population = selection(population, fitness)

        # 交叉操作
        new_population = []
        for i in range(0, NP, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            new_population.append(child1)
            new_population.append(child2)

        # 变异操作
        for i in range(NP):
            new_population[i] = mutation(new_population[i])

        population = new_population

    return best_individual, best_fitness, history


# 运行遗传算法
best_path, best_length, history = genetic_algorithm()

# 结果可视化
plt.figure(figsize=(12, 5))

# 绘制路径图
plt.subplot(1, 2, 1)
x = [data[i][0] for i in best_path] + [data[best_path[0]][0]]
y = [data[i][1] for i in best_path] + [data[best_path[0]][1]]
plt.plot(x, y, 'o-')
plt.title(f"Best Path (Length={best_length:.4f})")
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# 绘制进化曲线
plt.subplot(1, 2, 2)
plt.plot(history, 'b-')
plt.title('Optimization Process')
plt.xlabel('Generation')
plt.ylabel('Shortest Path Length')
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"\nOptimal Path: {best_path}")
print(f"Shortest Distance: {best_length:.4f}")