import shelve
import re
import os
from tqdm import tqdm

char_list = open("输入法小作业/拼音汉字表/一二级汉字表.txt", 'r', encoding='gbk').read()


def build_dictionary(path):
    dictionary = {}
    lines = open(path, 'r', encoding='gbk').readlines()
    for line in tqdm(lines):
        line = line.strip()
        pinyin = line.split(' ')[0]
        for char in line.split(' ')[1:]:
            if char not in char_list:
                continue
            if pinyin in dictionary:
                dictionary[pinyin].append(char)
                # print("duplicate pinyin: " + pinyin)
            else:
                dictionary[pinyin] = [char]
                # print("new pinyin: " + pinyin)
        if not line:
            break
    return dictionary


def build_table_of_char(path, table_first, table, encoding='gbk'):
    corpus = open(path, 'r', encoding=encoding).read()
    pattern = '[\u4e00-\u9fa5]+'
    sentences = re.findall(pattern, corpus)
    for sentence in tqdm(sentences):

        char = sentence[0]

        if char in char_list:
            if char in table_first:
                table_first[char] += 1
            else:
                table_first[char] = 1

        for i in range(1, len(sentence)):
            if sentence[i] not in char_list:
                continue
            pre_char = sentence[i - 1]
            if pre_char not in char_list:
                continue
            if pre_char not in table:
                table[pre_char] = {}

            sub_table = table[pre_char]
            char = sentence[i]

            if char in sub_table:
                sub_table[char] += 1
            else:
                sub_table[char] = 1

    return table_first, table


def build_table():
    dic = build_dictionary("输入法小作业/拼音汉字表/拼音汉字表.txt")
    db = shelve.open('table')
    db['dictionary'] = dic
    print("build dictionary succeed!")
    table_at_first = {}
    table_all = {}

    for filepath, dirname, filename in os.walk("/Users/huing/学习/大二下/人智导/语料库"):
        for file in filename:
            if file == '.DS_Store':
                continue
            full_path = os.path.join(filepath, file)
            print("building table of " + full_path + " ...")
            if file[:5] == 'baike':
                table_at_first, table_all = build_table_of_char(full_path, table_at_first, table_all, encoding='utf-8')
            else:
                build_table_of_char(full_path, table_at_first, table_all)
            print("build table of " + full_path + " succeed!")
    db['table_at_first'] = table_at_first
    db['table_all'] = table_all
    db.close()
