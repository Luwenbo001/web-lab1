import csv
import numpy as np
import pandas as pd
from torch import nn
from tqdm import tqdm
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score
import time
start_time = time.time()
input = ["../data/index/selected_book_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_book_top_1200_data_tag_tokenized_pkuseg",
"../data/index/selected_movie_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_movie_top_1200_data_tag_tokenized_pkuseg"]

def getList(word):
    for i in range(4):
        file_dict = open(input[i] + "_basic_store_dict.binery_block", "rb")
        file_index = open(input[i] + "_basic_store_index.binery_block", "rb")
        dict_data = file_dict.read()
        index_data = file_index.read()
        dict_ptr = 0
        str_len = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
        dict_ptr += 4
        total_str = dict_data[dict_ptr : dict_ptr + str_len].decode()
        dict_ptr += str_len
        left = 0
        right =int( (len(dict_data)-left)//49 )
        while (left < right):
            mid = (left + right) // 2
            print(mid)
            print(left)
            print(right)
            str_ptr = int.from_bytes(dict_data[dict_ptr + mid * 49 : dict_ptr + mid * 49 + 4])
            str_len1 = int.from_bytes(dict_data[dict_ptr + mid * 49 + 4 : dict_ptr + mid * 49 + 5])
            word1_ = total_str[str_ptr : str_ptr + str_len1]
            mid1= mid+1
            str_ptr = int.from_bytes(dict_data[dict_ptr + mid1 * 49 : dict_ptr + mid1 * 49 + 4])
            str_len1 = int.from_bytes(dict_data[dict_ptr + mid1 * 49 + 4 : dict_ptr + mid1 * 49 + 5])
            word2_ = total_str[str_ptr : str_ptr + str_len1]
            if (word1_ <= word < word2_):
                k = 0
                for i in range(5):
                    str_ptr = int.from_bytes(dict_data[dict_ptr + mid * 49 : dict_ptr + mid * 49 + 4])
                    str_len = int.from_bytes(dict_data[dict_ptr + mid * 49 + 9*i + 4 : dict_ptr + mid * 49 + 9*i + 5])
                    
                    word0_ = total_str[str_ptr +k: str_ptr + k+ str_len]
                    k += str_len
                    if (word0_ == word):
                        freq = int.from_bytes(dict_data[dict_ptr + mid * 49 + 9*i + 5 : dict_ptr + mid * 49 + 9*i + 9])
                        index_ptr = int.from_bytes(dict_data[dict_ptr + mid * 49 + 9*i + 9 : dict_ptr + mid * 49 + 9*i + 13])
                        index = []
                        for i in range(0, freq):
                            index.append(int.from_bytes(index_data[index_ptr : index_ptr + 4]))
                            index_ptr += 4
                        return index
            elif (word2_ <= word):#当中值小于目标值 说明应该在右边查找了
                left = mid + 1 #把左索引 变成mid+1
            else:#当中值大于目标值 说明应该在左边查找了
                right = mid - 1 #把右索引 变成mid-1
        # j = 0
        # with open(input[i], 'r', encoding='gbk', errors='ignore') as file:
        #     for line in file:
        #         j+=1# 去除每行末尾的换行符（如果有的话）
        #         line = line.rstrip()
        #         prefix = line.split()[0]
        #         if (word == prefix):
        #             k=0
        #             with open(input[i+4], 'r', encoding='gbk', errors='ignore') as file1:
        #                 for line in file1:
        #                     k+=1
        #                     line = line.rstrip()
        #                     if (j == k) :
        #                         cleaned_text = line[1:-1]
        #                         real_array = cleaned_text.split(',')
        #                         real_array = [int(x) for x in real_array]
        #                         return real_array
        
    
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
#print('美丽 AND 鲨鱼 AND 中文 AND 村上:', And(getList('鲨鱼'),And(getList('村上'),And(getList('中文'), getList('美丽')))))
#print('! AND !!:', And(getList('!'), getList('!!')))
#print('(! AND !!)OR(2 AND 1 ):', Or(And(getList('!'), getList('!!')),And(getList('2'), getList('1'))))
print('(中文 OR 人生)ANDNOT(信息 AND 作业):', AndNot(Or((getList('中文')), getList('人生')),And(getList('信息'), getList('作业'))))
end_time = time.time()
running_time = end_time-start_time

print('程序运行时间：', running_time, '秒')