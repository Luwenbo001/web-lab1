def write_index_block(file_path, inverted_index):  #需要分开存储词典和倒排表项
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
    str_pt = 0
    k = 5   #每k个词项存储一个指针
    # file_words = open(file_path + "_words.binery", "wb")
    # file_words.write(wordssum.encode())
    # file_dict = open(file_path + "_dict.binery", "wb")
    # file_index = open(file_path + "_index.binery", "wb")
    file1 = open(file_path + "_basic_store_dict.binery_block", "wb")
    file2 = open(file_path + "_basic_store_index.binery_block", "wb")
    total_str = ""
    for index,(key, value) in enumerate(inverted_index):
        total_str += key
        
    file1.write(len(total_str.encode()).to_bytes(4)) #预先写入字符串长度
    dict_pt += 4
    file1.seek(dict_pt)
    file1.write(total_str.encode()) #写入整个字符串
    dict_pt += len(total_str.encode())
    file1.seek(dict_pt)
    for index,(key, value) in enumerate(inverted_index):
        if(index % 5 == 0):
            file1.write(str_pt.to_bytes(4)) #写入词项在整个字符串中的指针
            dict_pt += 4
            file1.seek(dict_pt)
        str_pt += len(key)
        file1.write(len(key).to_bytes(1))   #写入词项长度
        dict_pt += 1
        file1.seek(dict_pt)
        file1.write(len(value).to_bytes(4)) #写入频率
        dict_pt += 4
        file1.seek(dict_pt)
        file1.write(index_pt.to_bytes(4))   #写入倒排索引表指针
        dict_pt += 4
        file1.seek(dict_pt)
        for id in value:
            file2.write(id.to_bytes(4))     #写入倒排索引表
            index_pt += 4
            file2.seek(index_pt)
    # with open(file_path + "_dict.csv", 'w', encoding='utf-8') as file:
    #     for key, value in inverted_index.items():
    #         print(key, ",", len(value), ",", value, file=file)
    # with open(file_path + "_index.csv", 'w', encoding='utf-8') as file:
    #     for key, value in inverted_index.items():
    #         print(key, ",", len(value), ",", value, file=file)
    return 