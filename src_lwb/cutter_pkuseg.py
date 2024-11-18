import csv
import pkuseg
book_data_path = "../data/selected_book_top_1200_data_tag.csv"
movie_data_path = "../data/selected_movie_top_1200_data_tag.csv"

book_reader = csv.reader(open(book_data_path, 'r'))
movie_reader = csv.reader(open(movie_data_path, 'r'))

book_column = 'Book,Tags'
movie_column = 'Movie,Tags'
book_content = []
movie_content = []

book_output_path = "../data/selected_book_top_1200_data_tag_tokenized_pkuseg.csv"
movie_output_path = "../data/selected_movie_top_1200_data_tag_tokenized_pkuseg.csv"

seg = pkuseg.pkuseg()

# for i,member in enumerate(book_reader):
#     if(i==0): continue
#     is_pair = 0
#     str = ""

#     book_output_row = ""
#     book_output_row += member[0] + "," + '"' + "{"

#     words = []
#     # print(member[1])
#     for ch in member[1]:
#         if((ch == "," or ch == '}')and is_pair == 1): 
#             is_pair = 0
#             words.append(str[:-1])
#             str = ""
#             continue
#         if(is_pair == 1):
#             str += ch
#         if(ch == "'" and is_pair == 0): is_pair = 1
#     token = []
#     for word in words:
#         tokens = seg.cut(word)
#         for token in tokens:
#             book_output_row += "'" + token + "'" + ","
#     book_output_row += "}" + '"' + "\n"
#     book_content.append(book_output_row)

# with open(book_output_path, 'w') as f:
#     f.write(book_column + "\n")
#     f.writelines(book_content)



for i,member in enumerate(movie_reader):
    if(i==0): continue
    is_pair = 0
    str = ""

    movie_output_row = ""
    movie_output_row += member[0] + "," + '"' + "{"

    words = []
    # print(member[1])
    for ch in member[1]:
        if((ch == "," or ch == '}')and is_pair == 1): 
            is_pair = 0
            words.append(str[:-1])
            str = ""
            continue
        if(is_pair == 1):
            str += ch
        if(ch == "'" and is_pair == 0): is_pair = 1
    token = []
    for word in words:
        tokens = seg.cut(word)
        for token in tokens:
            movie_output_row += "'" + token + "'" + ","
    movie_output_row += "}" + '"' + "\n"
    movie_content.append(movie_output_row)

with open(movie_output_path, 'w') as f:
    f.write(movie_column + "\n")
    f.writelines(movie_content)