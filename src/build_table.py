import re
import os
from tqdm import tqdm
import pickle


class BuildTable:
    base_dir: str
    char_list: str
    table_at_first = {}
    table_1_to_1 = {}
    table_2_to_1 = {}
    dictionary = {}

    def build_dictionary(self, path):
        print("start building dictionary...")
        lines = open(path, 'r', encoding='gbk').readlines()
        for line in tqdm(lines):
            line = line.strip()
            pinyin = line.split(' ')[0]
            for char in line.split(' ')[1:]:
                if char not in self.char_list:
                    continue
                if pinyin in self.dictionary:
                    self.dictionary[pinyin].append(char)
                else:
                    self.dictionary[pinyin] = [char]
            if not line:
                break
        return self.dictionary

    def build_table_of_char(self, path, encoding='gbk'):
        print("building table of " + path + " ..." + " encoding: " + encoding)
        corpus = open(path, 'r', encoding=encoding).read()
        pattern = '[\u4e00-\u9fa5]+'
        sentences = re.findall(pattern, corpus)
        for sentence in tqdm(sentences):

            char = sentence[0]

            if char in self.char_list:
                if char in self.table_at_first:
                    self.table_at_first[char] += 1
                else:
                    self.table_at_first[char] = 1

            # build table one char to one char
            for i in range(1, len(sentence)):
                if sentence[i] not in self.char_list:
                    continue

                pre_char = sentence[i - 1]
                char = sentence[i]

                # init the dict
                if pre_char not in self.table_1_to_1:
                    self.table_1_to_1[pre_char] = {}

                curr_dict = self.table_1_to_1[pre_char]

                if char in curr_dict:
                    curr_dict[char] += 1
                else:
                    curr_dict[char] = 1

            # build table two char to one char
            for i in range(2, len(sentence)):
                if sentence[i] not in self.char_list:
                    continue

                pre_two_char = sentence[i - 2] + sentence[i - 1]
                if pre_two_char not in self.table_2_to_1:
                    self.table_2_to_1[pre_two_char] = {}

                curr_dict = self.table_2_to_1[pre_two_char]
                char = sentence[i]

                if char in curr_dict:
                    curr_dict[char] += 1
                else:
                    curr_dict[char] = 1

    def build_table(self, path="输入法小作业", utf_list:list=None):
        if utf_list is None:
            utf_list = []
        if utf_list is None:
            utf_list = []
        self.base_dir = path
        self.char_list = open(self.base_dir + "/拼音汉字表/一二级汉字表.txt", 'r', encoding='gbk').read()
        print("start building table...")

        ignore_list = ['.DS_Store']
        utf_list.append('baike')

        dic_pkl = open('src/dictionary.pkl', 'wb')
        self.build_dictionary(self.base_dir + "/拼音汉字表/拼音汉字表.txt")
        pickle.dump(self.dictionary, dic_pkl)
        dic_pkl.close()
        print("build dictionary succeed!")

        # build count table
        count = 0
        print(f"{self.base_dir}" + "/语料库")
        for filepath, dirname, filename in os.walk(self.base_dir + "/语料库"):
            count += 1
            for file in filename:
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
                    self.build_table_of_char(full_path, encoding='utf-8')
                else:
                    self.build_table_of_char(full_path)
                print("build table of " + full_path + " succeed!")

        match_pkl = open('src/match.pkl', 'wb')
        pickle.dump([self.table_at_first, self.table_1_to_1, self.table_2_to_1], match_pkl)
        match_pkl.close()

        count_pkl = open('src/count.pkl', 'wb')
        table_one_count = {key: sum(self.table_1_to_1[key].values()) for key in self.table_1_to_1}
        table_two_count = {key: sum(self.table_2_to_1[key].values()) for key in self.table_2_to_1}
        pickle.dump([table_one_count, table_two_count], count_pkl)
