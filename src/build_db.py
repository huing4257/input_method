import shelve
import re
import os
from tqdm import tqdm

base_dir = "输入法小作业"
char_list = open(base_dir + "/拼音汉字表/一二级汉字表.txt", 'r', encoding='gbk').read()
table_at_first = {}
table_1_to_1 = {}
table_2_to_1 = {}
dictionary = {}


def build_dictionary(path):
    print("start building dictionary...")
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


def build_table_of_char(path, encoding='gbk'):
    print("building table of " + path + " ..." + " encoding: " + encoding)
    corpus = open(path, 'r', encoding=encoding).read()
    pattern = '[\u4e00-\u9fa5]+'
    sentences = re.findall(pattern, corpus)
    for sentence in tqdm(sentences):

        char = sentence[0]

        if char in char_list:
            if char in table_at_first:
                table_at_first[char] += 1
            else:
                table_at_first[char] = 1

        # build table one char to one char
        for i in range(1, len(sentence)):
            if sentence[i] not in char_list:
                continue

            pre_char = sentence[i - 1]
            if pre_char not in table_1_to_1:
                table_1_to_1[pre_char] = {}

            curr_dict = table_1_to_1[pre_char]
            char = sentence[i]

            if char in curr_dict:
                curr_dict[char] += 1
            else:
                curr_dict[char] = 1

        # build table two char to one char
        for i in range(2, len(sentence)):
            if sentence[i] not in char_list:
                continue

            pre_two_char = sentence[i - 2] + sentence[i - 1]
            if pre_two_char not in table_2_to_1:
                table_2_to_1[pre_two_char] = {}

            curr_dict = table_2_to_1[pre_two_char]
            char = sentence[i]

            if char in curr_dict:
                curr_dict[char] += 1
            else:
                curr_dict[char] = 1


def build_table():
    ignore_list = ['.DS_Store']
    utf_list = ['baike', 'wiki']

    db = shelve.open('data/table')

    print("start building table...")

    build_dictionary(base_dir + "/拼音汉字表/拼音汉字表.txt")
    db['dictionary'] = dictionary
    print("build dictionary succeed!")

    for filepath, dirname, filename in os.walk(base_dir + "/语料库"):
        for file in filename[:1]:
            if file in ignore_list:
                continue
            full_path = os.path.join(filepath, file)
            # check if the file is utf-8
            is_utf = False
            for name in utf_list:
                if file.find(name) != -1:
                    is_utf = True
                    break

            if is_utf:
                build_table_of_char(full_path, encoding='utf-8')
            else:
                build_table_of_char(full_path)
            print("build table of " + full_path + " succeed!")
        is_continue = input("continue? (y/n)")
        if is_continue == 'n':
            break

    db['table_at_first'] = table_at_first
    db['table_2_to_1'] = table_2_to_1
    db['table_1_to_1'] = table_1_to_1
    db.close()
