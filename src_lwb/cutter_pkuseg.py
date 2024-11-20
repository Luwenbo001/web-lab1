import csv
import pkuseg
import time
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

bad_list = [' ','【','】','[',']','-','+','/','、','，','。','：','；','“','”','《','》','？','！','@','#','$','%','^','&','*','(',')','_','+','=','{','}','|','\\',';',':','\'','"','<','>','/','?','~','`','的','吗','里','还','行','而','覺得','片','这个','我','个','.','（','）','和','是','有','在','对','了','就','也','／','’','‘']

T1 = time.time()
for i,member in enumerate(book_reader):
    if(i==0): continue
    is_pair = 0
    str = ""

    book_output_row = ""
    book_output_row += member[0] + "," + '"' + "{"

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
            f = 0
            for bad in bad_list:
                if(token == bad):
                    f = 1
                    break
            if(f == 0): 
                book_output_row += "'" + token + "'" + ","
    book_output_row += "}" + '"' + "\n"
    book_content.append(book_output_row)

T2 = time.time()
print("pkuseg book time: ", T2-T1)
with open(book_output_path, 'w') as f:
    f.write(book_column + "\n")
    f.writelines(book_content)



T1 = time.time()
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
            f = 0
            for bad in bad_list:
                if(token == bad):
                    f = 1
                    break
            if(f == 0): 
                movie_output_row += "'" + token + "'" + ","
    movie_output_row += "}" + '"' + "\n"
    movie_content.append(movie_output_row)

T2 = time.time()
print("pkuseg movie time: ", T2-T1)
with open(movie_output_path, 'w') as f:
    f.write(movie_column + "\n")
    f.writelines(movie_content)