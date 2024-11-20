import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

input = ["../data/index/selected_book_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_book_top_1200_data_tag_tokenized_pkuseg",
"../data/index/selected_movie_top_1200_data_tag_tokenized_jieba",
"../data/index/selected_movie_top_1200_data_tag_tokenized_pkuseg"]
output = ["../data/index/testread/selected_book_top_1200_data_tag_tokenized_jieba",
"../data/index/testread/selected_book_top_1200_data_tag_tokenized_pkuseg",
"../data/index/testread/selected_movie_top_1200_data_tag_tokenized_jieba",
"../data/index/testread/selected_movie_top_1200_data_tag_tokenized_pkuseg"]

def process(i):
    file_dict = open(input[i] + "_basic_store_dict.binery_single", "rb")
    file_index = open(input[i] + "_basic_store_index.binery_single", "rb")
    file_dict_out = open(output[i] + "_dict_single.txt", "w", encoding="utf-8")
    file_index_out = open(output[i] + "_index_single.txt", "w", encoding="utf-8")

    dict_data = file_dict.read()
    index_data = file_index.read()

    dict_ptr = 0
    index_ptr = 0
    print(len(dict_data))
    str_len = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
    dict_ptr += 4
    total_str = dict_data[dict_ptr : dict_ptr + str_len].decode()
    dict_ptr += str_len
    while (dict_ptr < len(dict_data)):
        str_ptr = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
        freq = int.from_bytes(dict_data[dict_ptr + 4 : dict_ptr + 8])
        pindex = int.from_bytes(dict_data[dict_ptr + 8 : dict_ptr + 12])
        dict_ptr += 12
        if (dict_ptr >= len(dict_data)):
            new_str_ptr = str_len
        else:
            new_str_ptr = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
        print(total_str[str_ptr : new_str_ptr], freq, pindex, file=file_dict_out)
        index = []
        for i in range(0, freq):
            index.append(int.from_bytes(index_data[index_ptr : index_ptr + 4]))
            index_ptr += 4
        print(index, file=file_index_out)
        
def main():
    for i in range(4):
        process(i)

if __name__ == "__main__":
    main()
        