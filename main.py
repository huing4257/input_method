import os
import re
import shelve

import numpy as np

from build_db import build_table

if __name__ == '__main__':

    if not os.path.exists('table.db'):
        build_table()  # requires Directory 输入法小作业 in root path
    print('build table succeed! \n')

    table_at_first = shelve.open('table').get('table_at_first')
    table_all = shelve.open('table').get('table_all')
    dictionary = shelve.open('table').get('dictionary')

    # assert type of dicts get from shelve to avoid warning
    assert isinstance(dictionary, dict)
    assert isinstance(table_at_first, dict)
    assert isinstance(table_all, dict)

    output = open('output.txt', 'w', encoding='gbk')

    with open('input.txt', 'r', encoding='gbk') as f:
        lines = f.readlines()
        for line in lines:
            p_list = re.split(r'[\n, ]', line.strip())
            choices_lists = []
            for pinyin in p_list:
                choices_lists.append(dictionary[pinyin])

            num_step = len(choices_lists)

            # 初始化DP矩阵
            dp = [np.zeros(len(choices_lists[i]), dtype=np.float64) for i in range(num_step)]
            dp[0] = np.array([table_at_first.get(char, 0.0001) for char in choices_lists[0]], dtype=np.float64)
            dp[0] /= sum(dp[0])
            dp[0] = np.log(dp[0])

            # 用于存储前一个时间步长的最优预测
            pred = np.array([[0] * len(choices_lists[i]) for i in range(num_step)])

            # 动态规划
            for i in range(1, num_step):
                for j in range(0, len(choices_lists[i])):
                    max_log_prob = -np.inf
                    for k in range(len(choices_lists[i - 1])):
                        whole_set = table_all.get(choices_lists[i - 1][k], {})
                        if whole_set == {}:
                            continue
                        sum_value = sum(whole_set.values())
                        log_prob = dp[i - 1][k] + np.log(whole_set.get(choices_lists[i][j], 0.0001) / sum_value)
                        if log_prob > max_log_prob:
                            max_log_prob = log_prob
                            pred[i][j] = k
                    dp[i][j] = max_log_prob

            # 回溯，找出最优路径
            k = 0
            for i in range(len(dp[-1])):
                if dp[-1][i] >= dp[-1][k]:
                    k = i
            ret = choices_lists[num_step - 1][k]
            for i in range(0, num_step - 1)[::-1]:
                k = pred[i + 1][k]
                ret = choices_lists[i][k] + ret

            # 输出最优路径
            output.write(ret + '\n')
