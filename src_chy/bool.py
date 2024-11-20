import csv
import numpy as np
import pandas as pd
from torch import nn
from tqdm import tqdm
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score
input = ["data/index/testread/selected_book_top_1200_data_tag_tokenized_jieba_dict.txt",
"data/index/testread/selected_book_top_1200_data_tag_tokenized_pkuseg_dict.txt",
"data/index/testread/selected_movie_top_1200_data_tag_tokenized_jieba_dict.txt",
"data/index/testread/selected_movie_top_1200_data_tag_tokenized_pkuseg_dict.txt",
"data/index/testread/selected_book_top_1200_data_tag_tokenized_jieba_index.txt",
"data/index/testread/selected_book_top_1200_data_tag_tokenized_pkuseg_index.txt",
"data/index/testread/selected_movie_top_1200_data_tag_tokenized_jieba_index.txt",
"data/index/testread/selected_movie_top_1200_data_tag_tokenized_pkuseg_index.txt",]
def getList(word):
    prefixes = []
    linetext = []
    for i in range(4):
        j = 0
        with open(input[i], 'r', encoding='gbk', errors='ignore') as file:
            for line in file:
                j+=1# 去除每行末尾的换行符（如果有的话）
                line = line.rstrip()
                prefix = line.split()[0]
                if (word == prefix):
                    k=0
                    with open(input[i+4], 'r', encoding='gbk', errors='ignore') as file1:
                        for line in file1:
                            k+=1
                            line = line.rstrip()
                            if (j == k) :
                                cleaned_text = line[1:-1]
                                real_array = cleaned_text.split(',')
                                real_array = [int(x) for x in real_array]
                                return real_array
        
    
def And(list1, list2):
    i, j = 0, 0
    res = []
    while i < len(list1) and j < len(list2):
        # 同时出现，加入结果列表
        if list1[i] == list2[j]:
            res.append(list1[i])
            i += 1
            j += 1
        # 指向较小数的指针后移
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return res

def Or(list1, list2):
    i, j = 0, 0
    res = []
    while i < len(list1) and j < len(list2):
        # 同时出现，只需要加入一次
        if list1[i] == list2[j]:
            res.append(list1[i])
            i += 1
            j += 1
        # 指向较小数的指针后移，并加入列表
        elif list1[i] < list2[j]:
            res.append(list1[i])
            i += 1
        else:
            res.append(list2[j])
            j += 1
    # 加入未遍历到的index
    res.extend(list1[i:]) if j == len(list2) else res.extend(list2[j:])
    return res

def AndNot(list1, list2):
    i, j = 0, 0
    res = []
    while i < len(list1) and j < len(list2):
        # index相等时，同时后移
        if list1[i] == list2[j]:
            i += 1
            j += 1
        # 指向list1的index较小时，加入结果列表
        elif list1[i] < list2[j]:
            res.append(list1[i])
            i += 1
        else:
            j += 1
    # list1 未遍历完，加入剩余index
    if i != len(list1):
        res.extend(list1[i:])
    return res

print('! AND !!:', And(getList('!'), getList('!!')))

