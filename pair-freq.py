import re
from collections import defaultdict


def process_data(input_file, output_file):
    # 字母对频率统计
    letter_pair_freq = defaultdict(int)

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # 跳过表头
        for line in lines[9:]:
            # 按制表符分割列
            columns = line.strip().split('\t')

            # 跳过空行或格式问题的行
            if len(columns) < 4:
                continue

            # 获取单词和频率
            word = columns[1].strip().lower()  # 忽略大小写
            try:
                freq = int(columns[3].strip())  # 获取单词频率
            except ValueError:
                continue

            # 提取单词中的连续字母对
            for i in range(len(word) - 1):
                pair = word[i:i+2]  # 字母对
                if pair.isalpha():  # 只保留字母
                    letter_pair_freq[pair] += freq  # 累计频率

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Pair\tFrequency\n")
        for pair, freq in sorted(letter_pair_freq.items()):
            out_file.write(f"{pair}\t{freq}\n")


# 输入文件名和输出文件名
input_file = 'lemmas_60k.txt'
output_file = 'pair-freq.txt'

# 调用函数处理数据
process_data(input_file, output_file)
