# INPUT METHOD
## 1. Introduction
本仓库为2023年春季学期人工智能导论课程的大作业，主要内容为实现一个输入法。
## 2. Usage
### 2.1. Environment
- Python 3.9
- numpy
- tqdm
### 2.2. File Structure
### 文件说明

   + 文件结构如下

   ```
       .
       |____requirements.txt
       |____README.md
       |____输入法小作业
       |____data
       | |____input.txt
       | |____output.txt
       |____src
         |____test.py
         |____build_db.py
         |____train.py
         |____main.py
         |____match.pkl
         |____count.pkl
         |____dictionary.pkl
         
   ```

+ match.pkl由于体积过大，以云盘的方式上传

   ### 数据说明

   + 若要训练数据，需使得“输入法小作业”文件夹在项目根目录下，或指定一个包含以下文件的文件夹路径，并将需要训练的语料库放在“语料库”文件夹中
   
     ```
     .
     |____语料库
     |____拼音汉字表
       |____拼音汉字表.txt
       |____一二级汉字表.txt
     ```
### 2.3. Run
1. train
    ```bash
    python src/train.py [--dir <path to data folder>] [--utf_list <filename1,filenam2,...>]
    ```
2. run
    ```bash
    python src/main.py [--input <input file>] [--output <output file>] [-p] 
    ```
3. test
    ```bash
    python src/test.py
    ```

