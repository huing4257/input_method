import re
import pickle
import numpy as np
import argparse

# const value
CHAR_COEF = 8
WORD_COEF = 3


def get_output_line():
    p_list = re.split(r'[\n, ]', line.strip())
    steps = []

    for pinyin in p_list:
        try:
            steps.append(dictionary[pinyin])
        except KeyError:
            print("pinyin not found: " + pinyin)
            return ''

    num_step = len(steps)
    # store the best path
    pred = [np.zeros(len(steps[i]), dtype=int) for i in range(num_step)]
    # build dp table
    dp = [np.zeros(len(steps[i]), dtype=np.float64) for i in range(num_step)]
    # init dp[0]
    dp[0] = np.array([table_at_first.get(char, 0.00000001) for char in steps[0]], dtype=np.float64)
    dp[0] /= sum(dp[0])
    dp[0] = np.log(dp[0])
    # init dp[1]
    for i in range(len(steps[1])):
        max_log_prob = -np.inf
        for j in range(len(steps[0])):
            whole_set = table_1_to_1.get(steps[0][j], {})
            if whole_set == {}:
                continue
            sum_value = table_one_count[steps[0][j]]
            log_prob = dp[0][j] + np.log(whole_set.get(steps[1][i], 0.00000001) / sum_value)
            if log_prob > max_log_prob:
                max_log_prob = log_prob
                pred[1][i] = j
        dp[1][i] = max_log_prob
    # calculate dp[2:] using 3-gram
    for i in range(2, num_step):
        for j in range(0, len(steps[i])):
            max_log_prob = -np.inf
            for k in range(0, len(steps[i - 1])):
                whole_set = table_2_to_1.get(steps[i - 2][pred[i - 1][k]] + steps[i - 1][k], {})
                if whole_set == {}:
                    continue
                sum_value = table_two_count[steps[i - 2][pred[i - 1][k]] + steps[i - 1][k]]
                log_prob = dp[i - 1][k] + np.log(whole_set.get(steps[i][j], 0.00000001) / sum_value) + np.log(
                    table_one_count.get(steps[i][j], 0.00000001) / sum_of_one_count) / CHAR_COEF + np.log(
                    table_two_count.get(steps[i - 1][k] + steps[i][j], 0.00000001) / sum_of_two_count
                ) / WORD_COEF
                if log_prob > max_log_prob:
                    max_log_prob = log_prob
                    pred[i][j] = k
            dp[i][j] = max_log_prob
    # find the best path
    k: int = 0
    for i in range(len(dp[-1])):
        if dp[-1][i] >= dp[-1][k]:
            k = i
    ret_line: str = steps[num_step - 1][k]
    for i in range(0, num_step - 1)[::-1]:
        k = pred[i + 1][k]
        ret_line = steps[i][k] + ret_line
    return ret_line


if __name__ == '__main__':

    print("Loading data...")

    # read args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file path', default='data/input.txt')
    parser.add_argument('-o', '--output', help='output file path', default='data/output.txt')
    # play mode
    parser.add_argument('-p', '--play', help='play mode', action='store_true')
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    try:
        dictionary = pickle.load(open('src/dictionary.pkl', 'rb'))
        table_at_first, table_1_to_1, table_2_to_1 = pickle.load(open('src/match.pkl', 'rb'))
        table_one_count, table_two_count = pickle.load(open('src/count.pkl', 'rb'))
    except FileNotFoundError:
        print("Please run train.py first!")
        exit(0)

    sum_of_one_count = sum(table_one_count.values())
    sum_of_two_count = sum(table_two_count.values())

    # assert type of dicts get from shelve to avoid warning
    assert isinstance(dictionary, dict)
    assert isinstance(table_at_first, dict)
    assert isinstance(table_1_to_1, dict)
    assert isinstance(table_2_to_1, dict)
    assert isinstance(table_one_count, dict)
    assert isinstance(table_two_count, dict)

    # play mode
    if args.play:
        print('输入exit退出')
        while True:
            line = input('请输入拼音：')
            if line == 'exit':
                break
            print(get_output_line())
        exit(0)

    output = open(output_path, 'w', encoding='utf-8')
    with open(input_path, 'r', encoding='gbk') as f:
        lines = f.readlines()
        for line in lines:
            ret = get_output_line()
            # write to file
            output.write(ret + '\n')
