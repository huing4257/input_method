from build_table import BuildTable
# use std lib read the arguments
import argparse

parser = argparse.ArgumentParser(description='Train the model')
parser.add_argument('--dir', type=str, default='输入法小作业', help='the directory of the corpus')
parser.add_argument('--utf', type=str, default='baike', help='the list of filename encoded by utf, split by ","')
args = parser.parse_args()
base_dir = args.dir
utf_list = args.utf.split(',')

BuildTable().build_table(base_dir, utf_list)
