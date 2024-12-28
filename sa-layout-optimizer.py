import random
import math
from layout_assess import calculate_weighted_equivalence
import numpy as np


def generate_initial_layout():
    """生成初始键盘布局（QWERTY布局）。"""
    qwerty = "abcdefghijklmnopqrstuvwxyz"
    return {char: char for char in qwerty}


def pretty_format_layout(layout):
    """
    美化输出一个布局。
    """
    row1 = 'qwertyuiop'
    row2 = 'asdfghjkl'
    row3 = 'zxcvbnm'

    pos_dict = {j: i for i, j in layout.items()}

    new_rows = [
        ''.join(pos_dict[c] for c in row) for row in [row1, row2, row3]
    ]

    return '\n'.join(new_rows)


def generate_neighbor_layout(layout, max_swap_cnt=5):
    """
    通过随机交换至多 max_swap_cnt 个键位，生成一个邻居布局。
    """
    new_layout = layout.copy()
    keys = list(new_layout.keys())

    swap_cnt = random.randint(1, max_swap_cnt)

    for _ in range(swap_cnt):
        key1, key2 = random.sample(keys, 2)
        new_layout[key1], new_layout[key2] = new_layout[key2], new_layout[key1]

    return new_layout


def simulated_annealing(freq_file, pair_equivalence_file, initial_temp, cooling_rate, max_iter):
    """
    使用模拟退火算法优化键盘布局。

    参数:
    - freq_file: 字母对出现频率文件名
    - pair_equivalence_file: 字母对速度当量文件名
    - initial_temp: 初始温度
    - cooling_rate: 降温速率
    - max_iter: 每轮温度下的最大迭代次数

    返回:
    - 最优键盘布局及其对应的目标函数值。
    """
    # 初始化布局和目标函数值
    current_layout = generate_initial_layout()
    current_cost = calculate_weighted_equivalence(
        freq_file, pair_equivalence_file, current_layout)

    best_layout = current_layout
    best_cost = current_cost

    temperature = initial_temp
    outer_iter = 0
    cost_history = []

    while temperature > 1e-6:  # 温度足够低时停止
        outer_iter += 1
        print(f"===== Temperature: {temperature}")
        print(f"===== Outer Iteration: {outer_iter}")
        for _ in range(max_iter):
            # 生成新布局
            new_layout = generate_neighbor_layout(current_layout)
            new_cost = calculate_weighted_equivalence(
                freq_file, pair_equivalence_file, new_layout)

            # 判断是否接受新布局
            cost_diff = new_cost - current_cost
            if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
                current_layout = new_layout
                current_cost = new_cost

                # 更新全局最优解
                if new_cost < best_cost:
                    best_layout = new_layout
                    best_cost = new_cost

        # print(f"== Best Layout: ")
        # print(pretty_format_layout(best_layout))
        # print(f"== Best Cost: {best_cost}")
        cost_history.append(current_cost)

        # 降低温度
        temperature *= cooling_rate

    return best_layout, best_cost, cost_history


def make_plot(cost_history, initial_temp, cooling_rate):
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'Source Han Sans CN'

    iters = range(1, len(cost_history)+1)
    temperatures = [initial_temp*cooling_rate**i for i in iters]
    best_cost_hist = np.minimum.accumulate(cost_history)

    plt.figure(figsize=(6, 3))
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(iters, cost_history, color='lime', label="当前方案加权平均键位速度当量")
    ax1.plot(iters, best_cost_hist, color='purple', label="最佳方案加权平均键位速度当量")
    ax2.plot(iters, temperatures, color='red', label="温度")

    ax1.set_xlabel("外层迭代次数")
    ax1.set_ylabel("方案加权平均键位速度当量")
    ax2.set_ylabel("温度")

    fig.legend()
    fig.savefig("../report/fig-t2-sa.svg", bbox_inches='tight')
    fig.show()


# 开始实验
if __name__ == "__main__":
    # 输入文件名
    freq_file = "pair-freq.txt"  # 字母对频率文件
    pair_equivalence_file = "pair_equivalence.txt"  # 键位速度当量文件

    # 模拟退火参数
    initial_temp = 1000  # 初始温度
    cooling_rate = 0.95  # 降温速率
    max_iter = 100  # 每轮温度下的最大迭代次数

    # 调用模拟退火算法
    optimal_layout, optimal_cost, cost_history = simulated_annealing(
        freq_file, pair_equivalence_file, initial_temp, cooling_rate, max_iter
    )

    # 输出结果
    print("最优键盘布局:", optimal_layout)
    print(pretty_format_layout(optimal_layout))
    print("对应的加权平均键位速度当量:", optimal_cost)

    make_plot(cost_history, initial_temp, cooling_rate)
