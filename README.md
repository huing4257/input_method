# INPUT METHOD
##  Introduction

本仓库为2023年春季学期人工智能导论课程的小作业，主要内容为实现一个输入法。
## Environment

- Python 3.9
- numpy
- tqdm
## File Structure

### 文件结构

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

+ 若要训练数据，需使得“输入法小作业”文件夹在项目根目录下，或指定一个包含以下文件的文件夹路径，并将需要训练的语料库放在“语料库”文件夹中（测试时所使用的为新浪新闻、微博和百科问答语料库）

  ```
  .
  |____语料库
  |____拼音汉字表
    |____拼音汉字表.txt
    |____一二级汉字表.txt
  ```

## Usage

### Run 

1. train
    ```bash
    python src/train.py [-h] [--dir DIR] [--utf UTF]
    
    Train the model
    
    options:
      -h, --help  show this help message and exit
      --dir DIR   the directory of the corpus
      --utf UTF   the list of filename encoded by utf, split by ","
    ```
2. run
    ```bash
    python src/main.py [-h] [-i INPUT] [-o OUTPUT] [-p]
    
    options:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            input file path
      -o OUTPUT, --output OUTPUT
                            output file path
      -p, --play            play mode
    ```
3. test
    ```bash
    python src/test.py
    ```

