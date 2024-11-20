import csv

inverted_index = {}
# wordssum = ""
input = ["../data/selected_book_top_1200_data_tag_tokenized_jieba.csv",
"../data/selected_book_top_1200_data_tag_tokenized_pkuseg.csv",
"../data/selected_movie_top_1200_data_tag_tokenized_jieba.csv",
"../data/selected_movie_top_1200_data_tag_tokenized_pkuseg.csv"]
input_test = "../data/test.csv"
output = ["../data/index/selected_book_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_book_top_1200_data_tag_tokenized_pkuseg",
"../data/index/selected_movie_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_movie_top_1200_data_tag_tokenized_pkuseg"]

def process_csv(file_path):
    global inverted_index
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i,text in enumerate(reader):
            insert_line(i, text)
            
    for key, value in inverted_index.items():
        value.sort()    #对字典中的每一个列表进行排序
        
    inverted_index = sorted(inverted_index.items(), key=lambda d:d[0]) 

def insert_line(i, textline):
    global inverted_index
    if i == 0:
        return
    
    index = int(textline[0])    #book id
    words = []                  #tags
    is_pair = 0
    str = ""

    for ch in textline[1]:
        if((ch == "," or ch == '}')and is_pair == 1): 
            is_pair = 0
            words.append(str[:-1])
            str = ""
            continue
        if(is_pair == 1):
            str += ch
        if(ch == "'" and is_pair == 0): is_pair = 1
    for word in words:
        set = inverted_index.setdefault(word, [])   #不使用三步走，直接使用字典+列表
        set.append(index)
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

