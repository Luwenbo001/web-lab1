import csv
import word_compress_store_single_str
import word_compress_store_block

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
        
def write_index_normal(file_path):  #需要分开存储词典和倒排表项
    global inverted_index
    # maxlen = 0
    # word = ""
    # for key, value in inverted_index:
    #     if maxlen < len(key.encode()):
    #         maxlen = len(key.encode())
    #         word = key
    # print(maxlen)
    # print(word)
    #测试得到最长词项为85字节，于是取88字节存储词项
    dict_pt = 0
    index_pt = 0
    # file_words = open(file_path + "_words.binery", "wb")
    # file_words.write(wordssum.encode())
    # file_dict = open(file_path + "_dict.binery", "wb")
    # file_index = open(file_path + "_index.binery", "wb")
    file1 = open(file_path + "_basic_store_dict.binery", "wb")
    file2 = open(file_path + "_basic_store_index.binery", "wb")
    for index,(key, value) in enumerate(inverted_index):
        word = key.encode() + (88 - len(key.encode())) * b'\x00'
        file1.write(word)
        dict_pt += 88
        file1.seek(dict_pt)
        file1.write(len(value).to_bytes(4))
        dict_pt += 4
        file1.seek(dict_pt)
        file1.write(index_pt.to_bytes(4))
        dict_pt += 4
        file1.seek(dict_pt)
        for id in value:
            file2.write(id.to_bytes(4))
            index_pt += 4
            file2.seek(index_pt)
    # with open(file_path + "_dict.csv", 'w', encoding='utf-8') as file:
    #     for key, value in inverted_index.items():
    #         print(key, ",", len(value), ",", value, file=file)
    # with open(file_path + "_index.csv", 'w', encoding='utf-8') as file:
    #     for key, value in inverted_index.items():
    #         print(key, ",", len(value), ",", value, file=file)
    return        

def main():
    global inverted_index
    for i in range(4):
        process_csv(input[i])
        write_index_normal(output[i])
        word_compress_store_single_str.write_index_single_str(output[i], inverted_index)
        word_compress_store_block.write_index_block(output[i], inverted_index)
        inverted_index = {}

if __name__ == "__main__":
    main()