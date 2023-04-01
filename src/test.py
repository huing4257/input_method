import re

my_output = open('data/output.txt', 'r', encoding='utf').read()
std_output = open('data/std_output.txt', 'r', encoding='utf').read()

my_output = re.split(r'\n', my_output)
std_output = re.split(r'\n', std_output)

compare = zip(my_output, std_output)
total = len(my_output)
s = 0
for item in compare:
    if item[0] == item[1]:
        s += 1
print(f"句准确率：{s / total}")

my_output = ''.join(my_output)
std_output = ''.join(std_output)
compare = zip(my_output, std_output)
total = len(my_output)
s = 0
for item in compare:
    if item[0] == item[1]:
        s += 1
print(f"字准确率：{s / total}")
