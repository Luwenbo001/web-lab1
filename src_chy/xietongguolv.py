import torch
import pickle
import numpy as np
import pandas as pd
from torch import nn
from tqdm import tqdm
from utils import collate_fn
from graph_rec_model import GraphRec
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device

# 读loaded_data取保存的 CSV 文件
loaded_data = pd.read_csv('data/book_score.csv')

# 显示加载的数据
print(loaded_data)

def create_id_mapping(id_list):
    # 从ID列表中删除重复项并创建一个排序的列表
    unique_ids = sorted(set(id_list))
    
    # 创建将原始ID映射到连续索引的字典
    id_to_idx = {id: idx for idx, id in enumerate(unique_ids, start = 1)}
    
    # 创建将连续索引映射回原始ID的字典
    idx_to_id = {idx: id for id, idx in id_to_idx.items()}
    
    return id_to_idx, idx_to_id

user_ids = loaded_data['User'].unique()
book_ids = loaded_data['Book'].unique()

user_to_idx, idx_to_user = create_id_mapping(user_ids)
book_to_idx, idx_to_book = create_id_mapping(book_ids)

u_items_list, i_users_list = [(0, 0)], [(0, 0)]
loaded_data['user_map'] = loaded_data['User'].map(user_to_idx)
loaded_data['book_map'] = loaded_data['Book'].map(book_to_idx)

# 按映射后的用户 ID 分组
grouped_user = loaded_data.groupby('user_map')
grouped_book = loaded_data.groupby('book_map')

# 遍历排序后的分组
for user, group in tqdm(grouped_user):
    books = group['book_map'].tolist()
    rates = group['Rate'].tolist()
    
    u_items_list.append([(book, rate) for book, rate in zip(books, rates)])

for book, group in tqdm(grouped_book):
    users = group['user_map'].tolist()
    rates = group['Rate'].tolist()
    
    i_users_list.append([(user, rate) for user, rate in zip(users, rates)])

class BookRatingDataset(Dataset):
	def __init__(self, data, user_to_idx, book_to_idx, u_items_list, i_users_list):
		self.data = data
		self.user_to_idx = user_to_idx
		self.book_to_idx = book_to_idx
		self.u_items_list = u_items_list
		self.i_users_list = i_users_list

	def __getitem__(self, index):
		row = self.data.iloc[index]
		user = self.user_to_idx[row['User']]
		book = self.book_to_idx[row['Book']]
		rating = row['Rate'].astype(np.float32)
		u_items = self.u_items_list[user]
		i_users = self.i_users_list[book]

		return (user, book, rating), u_items, i_users

	def __len__(self):
		return len(self.data)
	
# 划分训练集和测试集
train_data, test_data = train_test_split(loaded_data, test_size=0.5, random_state=42)

# 创建训练集和测试集的数据集对象
train_dataset = BookRatingDataset(train_data, user_to_idx, book_to_idx, u_items_list,  i_users_list)
test_dataset = BookRatingDataset(test_data, user_to_idx, book_to_idx, u_items_list,  i_users_list)

# 创建训练集和测试集的数据加载器
train_dataloader = DataLoader(train_dataset, batch_size=4096, shuffle=True, collate_fn = collate_fn, drop_last = True)
test_dataloader = DataLoader(test_dataset, batch_size=4096, shuffle=False, collate_fn = collate_fn, drop_last = True)

num_users = loaded_data['User'].nunique()  # 假设有1000个用户
num_books = loaded_data['Book'].nunique()   # 假设有500本书
embedding_dim = 32

model = GraphRec(num_users + 1, num_books + 1, 7, embedding_dim).to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-5)

train_data.to_csv('data/train_book_score.csv', index=False)
test_data.to_csv('data/test_book_score.csv', index=False)