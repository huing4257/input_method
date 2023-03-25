import os
for filepath, dirname, filename in os.walk("语料库"):
    for file in filename:
        full_path = os.path.join(filepath, file)
        print(dirname, file, filepath, full_path)