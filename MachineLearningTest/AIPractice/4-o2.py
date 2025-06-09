from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import time

# 加载数据
data_path = "./data"
data = loadmat(data_path + '/position.mat')
data = data['C']


# 计算城市间距离
def get_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


distance = np.array([[get_distance(i, j) for j in data] for i in data])

# 遗传算法参数
NP = 300  # 增大种群规模
N = 31  # 城市数量
G = 2500  # 增加进化代数
base_Pc = 0.85  # 基础交叉概率
base_Pm = 0.15  # 基础变异概率
tournament_size = 5  # 锦标赛选择的大小
elite_size = 10  # 精英保留数量
diversity_threshold = 0.1  # 多样性阈值
stagnation_generations = 100  # 停滞代数阈值
reset_ratio = 0.2  # 重置比例


# 计算路径总长度
def calc_path_length(path):
    total_distance = 0
    for i in range(N):
        total_distance += distance[path[i], path[(i + 1) % N]]
    return total_distance


# 初始化种群
def initialize_population():
    population = []
    for _ in range(NP):
        individual = list(range(N))
        random.shuffle(individual)
        population.append(individual)
    return population


# 锦标赛选择
def tournament_selection(population, fitness):
    selected = []
    for _ in range(NP):
        # 随机选择 tournament_size 个个体进行比赛
        candidates = random.sample(range(len(population)), tournament_size)
        candidate_fitness = [fitness[i] for i in candidates]
        # 选择适应度最高的（注意：适应度是路径长度的倒数，所以越大越好）
        winner = candidates[np.argmax(candidate_fitness)]
        selected.append(population[winner].copy())
    return selected


# 多种交叉算子

# 顺序交叉 (OX)
def order_crossover(parent1, parent2):
    size = len(parent1)
    # 随机选择两个交叉点
    point1 = random.randint(0, size - 1)
    point2 = random.randint(point1 + 1, size)

    # 初始化子代
    child1 = [-1] * size
    child2 = [-1] * size

    # 复制父代1的中间段到子代1
    child1[point1:point2] = parent1[point1:point2]
    # 复制父代2的中间段到子代2
    child2[point1:point2] = parent2[point1:point2]

    # 填充子代1的剩余位置
    current_pos = point2 % size
    for i in range(size):
        city = parent2[(point2 + i) % size]
        if city not in child1:
            child1[current_pos] = city
            current_pos = (current_pos + 1) % size

    # 填充子代2的剩余位置
    current_pos = point2 % size
    for i in range(size):
        city = parent1[(point2 + i) % size]
        if city not in child2:
            child2[current_pos] = city
            current_pos = (current_pos + 1) % size

    return child1, child2


# 循环交叉 (CX)
def cycle_crossover(parent1, parent2):
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size

    # 找到循环
    cycle = [-1] * size
    start = 0
    while start < size:
        if cycle[start] != -1:
            start += 1
            continue

        # 开始一个新的循环
        idx = start
        while True:
            cycle[idx] = start
            value = parent2[idx]
            idx = parent1.index(value)
            if idx == start:
                break

        start += 1

    # 创建子代
    for i in range(size):
        if cycle[i] % 2 == 0:  # 偶数循环
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        else:  # 奇数循环
            child1[i] = parent2[i]
            child2[i] = parent1[i]

    return child1, child2


# 多种变异算子

# 交换变异
def swap_mutation(individual):
    size = len(individual)
    # 随机选择两个不同的位置
    idx1, idx2 = random.sample(range(size), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual


# 逆转变异
def inversion_mutation(individual):
    size = len(individual)
    # 随机选择两个点
    point1 = random.randint(0, size - 1)
    point2 = random.randint(point1 + 1, size)

    # 反转中间段
    individual[point1:point2] = individual[point1:point2][::-1]
    return individual


# 插入变异
def insertion_mutation(individual):
    size = len(individual)
    # 随机选择两个不同的位置
    idx1, idx2 = random.sample(range(size), 2)
    city = individual.pop(idx1)
    individual.insert(idx2, city)
    return individual


# 2-opt局部优化
def two_opt(individual):
    size = len(individual)
    improved = True
    while improved:
        improved = False
        for i in range(size - 1):
            for j in range(i + 2, size + 1):
                # 计算当前边的距离
                a1, a2 = individual[i], individual[(i + 1) % size]
                b1, b2 = individual[j % size], individual[(j + 1) % size]

                # 计算交换后边的距离
                if distance[a1, a2] + distance[b1, b2] > distance[a1, b1] + distance[a2, b2]:
                    # 反转从i+1到j的序列
                    individual[i + 1:j] = individual[i + 1:j][::-1]
                    improved = True
        # 如果已经是最优，则提前退出
        if not improved:
            break
    return individual


# 计算种群多样性
def calculate_diversity(population):
    diversity = 0
    n = len(population)
    for i in range(n):
        for j in range(i + 1, n):
            # 计算两个个体之间的差异
            diff = sum(1 for k in range(N) if population[i][k] != population[j][k])
            diversity += diff / N  # 归一化差异
    return diversity / (n * (n - 1) / 2)  # 平均多样性


# 主遗传算法
def genetic_algorithm():
    # 初始化种群
    population = initialize_population()
    best_individual = None
    best_fitness = float('inf')
    history = []  # 记录每代最优解
    diversity_history = []  # 记录多样性变化
    last_improvement = 0  # 记录上次改进的代数
    start_time = time.time()

    # 迭代进化
    for generation in range(G):
        # 计算适应度 (路径长度的倒数)
        path_lengths = [calc_path_length(ind) for ind in population]
        fitness = [1 / pl for pl in path_lengths]

        # 更新全局最优解
        current_best_index = np.argmin(path_lengths)
        current_best_length = path_lengths[current_best_index]
        if current_best_length < best_fitness:
            best_fitness = current_best_length
            best_individual = population[current_best_index].copy()
            last_improvement = generation
            print(f"Generation {generation + 1}: New best length = {best_fitness:.4f}")

        history.append(best_fitness)
        diversity = calculate_diversity(population)
        diversity_history.append(diversity)

        # 自适应参数调整
        stagnation = generation - last_improvement
        # 如果停滞时间过长，增加变异率
        Pm = base_Pm + (0.3 - base_Pm) * min(1.0, stagnation / stagnation_generations)
        # 如果多样性过低，增加变异率
        Pm = max(Pm, base_Pm + (0.25 - base_Pm) * max(0, (diversity_threshold - diversity) / diversity_threshold))
        # 交叉概率随停滞时间减少
        Pc = base_Pc * max(0.7, 1 - min(1.0, stagnation / stagnation_generations) * 0.3)

        # 定期重置部分个体
        if generation > 0 and generation % 100 == 0 and stagnation > 50:
            print(f"Generation {generation + 1}: Performing partial reset...")
            # 保留精英
            elite_indices = np.argsort(path_lengths)[:elite_size]
            new_population = [population[i].copy() for i in elite_indices]

            # 创建新个体
            for _ in range(NP - elite_size):
                individual = list(range(N))
                random.shuffle(individual)
                new_population.append(individual)

            population = new_population
            # 重新计算适应度
            path_lengths = [calc_path_length(ind) for ind in population]
            fitness = [1 / pl for pl in path_lengths]

        # 精英保留
        elite_indices = np.argsort(path_lengths)[:elite_size]
        elite_population = [population[i].copy() for i in elite_indices]

        # 选择操作（锦标赛选择）
        selected_population = tournament_selection(population, fitness)

        # 交叉操作 - 随机选择交叉算子
        new_population = []
        for i in range(0, NP - elite_size, 2):
            if i + 1 >= len(selected_population):
                break

            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]

            if random.random() < Pc:
                # 随机选择交叉算子
                if random.random() < 0.7:
                    child1, child2 = order_crossover(parent1, parent2)
                else:
                    child1, child2 = cycle_crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            new_population.append(child1)
            new_population.append(child2)

        # 变异操作 - 随机选择变异算子
        for i in range(len(new_population)):
            if random.random() < Pm:
                # 随机选择变异算子
                r = random.random()
                if r < 0.4:
                    new_population[i] = swap_mutation(new_population[i])
                elif r < 0.7:
                    new_population[i] = inversion_mutation(new_population[i])
                else:
                    new_population[i] = insertion_mutation(new_population[i])

        # 对部分个体应用局部优化
        if generation % 50 == 0:
            # 对前20%的个体应用2-opt
            for i in range(int(len(new_population) * 0.2)):
                new_population[i] = two_opt(new_population[i])

        # 添加精英个体
        new_population.extend(elite_population)

        # 确保种群大小正确
        population = new_population[:NP]

    # 对最终最优解应用2-opt
    best_individual = two_opt(best_individual)
    best_fitness = calc_path_length(best_individual)

    end_time = time.time()
    print(f"\nTotal time: {end_time - start_time:.2f} seconds")
    return best_individual, best_fitness, history, diversity_history


# 运行遗传算法
best_path, best_length, history, diversity_history = genetic_algorithm()

# 结果可视化
plt.figure(figsize=(15, 10))

# 绘制路径图
plt.subplot(2, 2, 1)
x = [data[i][0] for i in best_path] + [data[best_path[0]][0]]
y = [data[i][1] for i in best_path] + [data[best_path[0]][1]]
plt.plot(x, y, 'o-')
plt.title(f"Optimized Path (Length={best_length:.4f})")
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)

# 绘制进化曲线
plt.subplot(2, 2, 2)
plt.plot(history, 'b-')
plt.title('Optimization Process')
plt.xlabel('Generation')
plt.ylabel('Shortest Path Length')
plt.grid(True)

# 绘制多样性变化
plt.subplot(2, 2, 3)
plt.plot(diversity_history, 'g-')
plt.title('Population Diversity')
plt.xlabel('Generation')
plt.ylabel('Diversity')
plt.grid(True)

# 绘制城市分布
plt.subplot(2, 2, 4)
x_all = [data[i][0] for i in range(N)]
y_all = [data[i][1] for i in range(N)]
plt.scatter(x_all, y_all, color='red')
for i, txt in enumerate(range(N)):
    plt.annotate(txt, (x_all[i], y_all[i]))
plt.title('City Locations')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)

plt.tight_layout()
plt.savefig('tsp_ga_optimization.png')
plt.show()

print(f"\nOptimal Path: {best_path}")
print(f"Shortest Distance: {best_length:.4f}")