import re


def calculate_weighted_equivalence(freq_file, pair_equivalence_file, new_layout):
    """
    计算新键盘布局的加权平均键位速度当量。

    参数:
    - freq_file: 字母对出现频率的文件名
    - pair_equivalence_file: 字母对速度当量文件名
    - new_layout: 新键盘布局，字典格式，例如 {"f": "e", "r": "p", ...}

    返回:
    - 加权平均键位速度当量（float）
    """
    # 读取字母对出现频率
    pair_freq = {}
    with open(freq_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:  # 跳过表头
            pair, freq = line.strip().split('\t')
            pair_freq[pair] = int(freq)

    # 归一化字母对频率
    total_freq = sum(pair_freq.values())
    normalized_freq = {pair: freq /
                       total_freq for pair, freq in pair_freq.items()}

    # 读取字母对速度当量
    pair_equivalence = {}
    with open(pair_equivalence_file, 'r', encoding='utf-8') as f:
        for line in f:
            pair, equivalence = line.strip().split()
            pair_equivalence[pair] = float(equivalence)

    # 计算新布局下的加权平均键位速度当量
    total_weighted_equivalence = 0.0
    for pair, freq in normalized_freq.items():
        # 根据新布局调整字母对
        transformed_pair = new_layout[pair[0]] + new_layout[pair[1]]

        # 获取该字母对的速度当量（如果不存在，则跳过）
        if transformed_pair in pair_equivalence:
            equivalence = pair_equivalence[transformed_pair]
            total_weighted_equivalence += freq * equivalence

    return total_weighted_equivalence


# 示例使用
if __name__ == "__main__":
    # 输入文件名
    freq_file = "pair-freq.txt"  # 从上一步生成的字母对频率文件
    pair_equivalence_file = "pair_equivalence.txt"  # 键位速度当量文件

    # 示例新键盘布局
    # new_layout = {
    #     "a": "q", "b": "w", "c": "e", "d": "r", "e": "t", "f": "y", "g": "u",
    #     "h": "i", "i": "o", "j": "p", "k": "a", "l": "s", "m": "d", "n": "f",
    #     "o": "g", "p": "h", "q": "j", "r": "k", "s": "l", "t": "z", "u": "x",
    #     "v": "c", "w": "v", "x": "b", "y": "n", "z": "m"
    # }

    new_layout = {
        "q": "q", "w": "w", "e": "e", "r": "r", "t": "t", "y": "y", "u": "u",
        "i": "i", "o": "o", "p": "p", "a": "a", "s": "s", "d": "d", "f": "f",
        "g": "g", "h": "h", "j": "j", "k": "k", "l": "l", "z": "z", "x": "x",
        "c": "c", "v": "v", "b": "b", "n": "n", "m": "m"
    }

    # 计算加权平均键位速度当量
    result = calculate_weighted_equivalence(
        freq_file, pair_equivalence_file, new_layout)
    print(f"加权平均键位速度当量: {result}")
