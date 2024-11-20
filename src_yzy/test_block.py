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
    file_dict = open(input[i] + "_basic_store_dict.binery_block", "rb")
    file_index = open(input[i] + "_basic_store_index.binery_block", "rb")
    file_dict_out = open(output[i] + "_dict_block.txt", "w", encoding="utf-8")
    file_index_out = open(output[i] + "_index_block.txt", "w", encoding="utf-8")

    dict_data = file_dict.read()
    index_data = file_index.read()

    dict_ptr = 0
    index_ptr = 0
    print(len(dict_data))
    str_len = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
    dict_ptr += 4
    total_str = dict_data[dict_ptr : dict_ptr + str_len].decode()
    dict_ptr += str_len
    word_index = 0
    str_ptr = 0
    while (dict_ptr < len(dict_data)):
        if word_index % 5 == 0:
            str_ptr = int.from_bytes(dict_data[dict_ptr : dict_ptr + 4])
            dict_ptr += 4
        word_len = int.from_bytes(dict_data[dict_ptr : dict_ptr + 1])
        freq = int.from_bytes(dict_data[dict_ptr + 1 : dict_ptr + 5])
        pindex = int.from_bytes(dict_data[dict_ptr + 5 : dict_ptr + 9])
        dict_ptr += 9
        print(total_str[str_ptr : str_ptr + word_len], freq, pindex, file=file_dict_out)
        str_ptr += word_len
        word_index += 1
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
        