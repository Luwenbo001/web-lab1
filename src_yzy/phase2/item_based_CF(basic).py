import math
import csv

# for data format:
#       user1   user2   user3
# item1 
# item2
# item3                         for example
# {{item1: {user1 : comment11, user2 : comment12...}},
#  {item2: {user1 : comment21, user2 : comment22...}},
#  {item3: {user1 : comment31, user2 : comment32...}},
#  ...}

input_train = "../../data/train_book_score.csv"
input_test = "../../data/test_book_score.csv"
output_path = "../../data/predicted_rank.txt"

class item_comments():
    
    def __init__(self, data):
        self.data = data
        self.aver = {}
        for i, (item, comment) in enumerate(self.data.items()):
            if i == 0:
                continue
            item_sum = 0.0  #评分总和
            com_sum = 0     #评分总数
            for user, value in comment.items():
                if (int(value) > -1):
                    item_sum += int(value)
                    com_sum += 1
            self.aver[item] = item_sum / com_sum
    
    def get_comment(self, item1):
        for item, comment in self.data.items():
            if item == item1:
                return comment
        return -1   #not found
        
    def pearson_sim(self, item1, item2):
        comment1 = self.get_comment(item1)
        aver1 = self.aver[item1]
        comment2 = self.get_comment(item2)
        aver2 = self.aver[item2]
        
        c = 0.0 #协方差
        v1 = 0.0
        v2 = 0.0    #标准差
        for item, value in comment1.items():
            for item_, value_ in comment2.items():
                if item == item_ and int(value) != -1 and int(value_) != -1 :
                    c += (float(value) - aver1) * (float(value_) - aver2)
                    v1 += pow((float(value) - aver1), 2)
                    v2 += pow((float(value_) - aver2), 2)
        v1 = pow(v1, 0.5)
        v2 = pow(v2, 0.5)
        
        if v1 == 0.0 or v2 == 0.0:  #没有相关项
            return 0
        else:
            return c / (v1 * v2)
        
    def predict_rank(self, item, user):
        numerator = 0.0     #分子
        denomintor = 0.0    #分母
        for item_, comment in self.data.items():
            if (item == item_):
                continue
            if (user in comment):
                p_s = self.pearson_sim(item, item_)
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
        for comment in reader:
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
        comments = sorted(comments.items(), key=lambda d: d[1], reverse=True)
    
    with open(output_path, 'r', encoding='utf-8') as output_file:
        for user, comments in user_comments.items():
            print(user, comments, file=output_file)
            
def main():
    data = import_data()
    comment_set = item_comments(data=data)
    test_predict(comment_set)
    
if __name__ == '__main__':
    main()