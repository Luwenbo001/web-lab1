import math
import csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

book_split_word_jieba_path = "../data/selected_book_top_1200_data_tag_tokenized_jieba.csv"
movie_split_word_jieba_path = "../data/selected_movie_top_1200_data_tag_tokenized_jieba.csv"

book_split_word_pkuseg_path = "../data/selected_book_top_1200_data_tag_tokenized_pkuseg.csv"
movie_split_word_pkuseg_path = "../data/selected_movie_top_1200_data_tag_tokenized_pkuseg.csv"

input_train = "../data/train_book_score.csv"
input_test = "../data/test_book_score.csv"
output_path = "../data/predicted_rank_plus.txt"
# Path: src_lwb/work.py
# 使用pkuseg对数据进行分词

tfidf_matrix = None
id_to_order = {}
def init(path):
    global tfidf_matrix
    global id_to_order
    split_word = csv.reader(open(path, 'r'))

    item_id =[]
    item_tags_list = []
    item_tags_str = []

    for i, member in enumerate(split_word):
        if(i == 0): continue
        is_pair = 0
        str = ""
        words = []
        item_tags_str.append("")
        item_tags_list.append([])

        for ch in member[1]:
            if((ch == "," or ch == '}')and is_pair == 1): 
                is_pair = 0
                words.append(str[:-1])
                item_tags_str[i-1] += str[:-1] + " "
                str = ""
                continue
            if(is_pair == 1):
                str += ch
            if(ch == "'" and is_pair == 0): is_pair = 1
        
        id_to_order[member[0]] = i-1
        item_id.append(member[0])
        item_tags_list[i-1].append(words)

    tfidf_vec = TfidfVectorizer()

    # 使用 fit_transform() 得到 TF-IDF 矩阵
    tfidf_matrix = tfidf_vec.fit_transform(item_tags_str)
    tfidf_matrix = tfidf_matrix.toarray()

# for data format:
#       user1   user2   user3
# item1 
# item2
# item3                         for example
# {{item1, {user1 : comment11, user2 : comment12...}},
#  {item2, {user1 : comment21, user2 : comment22...}},
#  {item3, {user1 : comment31, user2 : comment32...}},
#  ...}

class item_comments():
    
    def __init__(self, data):
        self.data = data
        self.aver = {}
        for item, comment in self.data.items():
            item_sum = 0.0  #评分总和
            com_sum = 0     #评分总数
            for user, value in comment.items():
                if (int(value) > -1):
                    item_sum += int(value)
                    com_sum += 1
            self.aver[item] = item_sum / com_sum
    # comment: {user1 : comment11, user2 : comment
    def get_comment(self, item1):
        for item, comment in self.data.items():
            if item == item1:
                return comment
        return -1   #not found

    # suppoese "item" is the id of the item
    def tf_idf_sim(self, item1, item2):
        global tfidf_matrix
        global id_to_order
        if(item1 not in id_to_order or item2 not in id_to_order):
            print("item not found in id_to_order")
            exit(0)
        order1 = id_to_order[item1]
        order2 = id_to_order[item2]
        return np.dot(tfidf_matrix[order1], tfidf_matrix[order2]) / (np.linalg.norm(tfidf_matrix[order1]) * np.linalg.norm(tfidf_matrix[order2]))
        
    def predict_rank(self, item, user):
        numerator = 0.0     #分子
        denomintor = 0.0    #分母
        for item_, comment in self.data.items():
            if (item == item_):
                continue
            if (user in comment):
                p_s = self.tf_idf_sim(item, item_)
                numerator += p_s * float(comment[user])
                denomintor += p_s
        
        if denomintor == 0:
            return -1   #unpredictable
        else:
            return numerator/denomintor
    
    def solution(self):
        ret_data = self.data
        for item, comment in self.data.items():
            for user, value in comment.items():
                if int(value) == -1:
                    ret_data[item].second[user] = self.predict_rank(item, user)
        return ret_data

def import_data():
    data = {}
    with open(input_train, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i,comment in enumerate(reader):
            if i == 0:
                continue
            user = comment[0]
            item = comment[1]
            value = comment[2]
            item_set = data.setdefault(item, {})
            item_set[user] = value
    # print(data)
    return data
    
def test_predict(comment_set : item_comments):
    user_comments = {}
    for item, comments in comment_set.data.items():
        for user, value in comments.items():
            user_comment = user_comments.setdefault(user, {})
            user_comment[item] = value
            
    with open(input_test, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, comment in enumerate(reader):
            if (i > 2000):
                break
            if i == 0:
                continue
            user_ = comment[0]
            item_ = comment[1]
            predict_value = comment_set.predict_rank(item_, user_)
            user_comments[user][item_] = predict_value
            print(user_, item_, predict_value)
    
    for user, comments in user_comments.items():
        comments = sorted(comments.items(), reverse=True)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for user, comments in user_comments.items():
            print(user, comments, file=output_file)
            
def main():
    init(book_split_word_pkuseg_path)
    data = import_data()
    comment_set = item_comments(data=data)
    test_predict(comment_set)
    
if __name__ == '__main__':
    main()