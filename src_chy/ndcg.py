import pandas as pd
import math
 
def calculate_gain(relevance_scores):
    return relevance_scores
 
def calculate_discount(positions):
    return [1 / math.log2(position + 1) for position in positions]
 
def calculate_dcg(relevance_scores, k=None):
    if k is not None:
        relevance_scores = relevance_scores[:k]
    gains = calculate_gain(relevance_scores)
    discounts = calculate_discount(range(1, len(gains) + 1))
    dcg = sum(gain * discount for gain, discount in zip(gains, discounts))
    return dcg
 
def calculate_idcg(relevance_scores, k=None):
    sorted_relevance = sorted(relevance_scores, reverse=True)
    return calculate_dcg(sorted_relevance, k)
 
def calculate_ndcg(relevance_scores, predicted_scores, k=None):
    # 根据预测评分对实际得分进行排序
    sorted_indices = sorted(range(len(predicted_scores)), key=lambda i: predicted_scores[i], reverse=True)
    sorted_relevance = [relevance_scores[i] for i in sorted_indices]
    
    # 计算DCG和IDCG
    dcg = calculate_dcg(sorted_relevance, k)
    idcg = calculate_idcg(relevance_scores, k)
    
    # 避免除以零
    if idcg == 0:
        return 0.0
    
    # 计算NDCG
    return dcg / idcg
 
predicted_scores_df =[]
actual_scores_df =[]
 
with open('data/predicted_rank_plus.txt', 'r') as file:
    # 读取文件的每一行
    for line in file:
        # 去除每行末尾的换行符并分割字符串
        parts = line.strip('()\n').split(',')
        
        # 确保行有足够的列（至少4列）
        if len(parts) >= 4:
            # 读取第三列和第四列（索引从0开始，所以第三列是索引2，第四列是索引3）
            third_column = parts[3].strip()  # strip() 用于去除可能存在的空格
            fourth_column = parts[4].strip()
            predicted_scores_df.append(fourth_column[1:-1])
            actual_scores_df.append(int(third_column[1:-1]))
        

# 假设两个文件都有一列名为'movie_id'用于匹配，以及'score'列分别存储预测评分和实际得分
# 这里我们简单假设数据已经对齐，即两个DataFrame按movie_id排序且一一对应
 
# 提取评分列


k = 2000
ndcg_value = calculate_ndcg(actual_scores_df, predicted_scores_df, k)
print(f"NDCG@{k}:", ndcg_value)
