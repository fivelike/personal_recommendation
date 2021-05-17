# -*-coding:utf8-*-
"""
author: fivelike
date: 2021.5.17
util function
"""

import os


def get_item_info(input_file):
    """
    get item info: [title, genre]
    :param input_file: item info file
    :return:
        a dict: key: itemid, value: [title, genre]
    """

    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1: -1])
        item_info[itemid] = [title,genre]
    fp.close()
    return item_info

def get_ave_score(input_file):
    """
    get item ave rating score
    :param input_file: user rating file
    :return:
        a dict: key: itemid, value: ave_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record_dict:
            record_dict[itemid] = [0,0]
        record_dict[itemid][0]+=1
        record_dict[itemid][1]+=rating
    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0],3)
    return score_dict

def get_train_data(input_file):
    """
    get train_data for LFM model
    :param input_file: user_item_rating file
    :return:
        a list: [(userid, itemid, label)]
    """
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    neg_dict = {}
    pos_dict = {}
    train_data = []
    linenum=0
    score_thr = 4.0
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        line = line.replace('\n','')
        if linenum==0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item)<4:
            continue
        userid, itemid, rating = item[0],item[1], float(item[2])
        if userid not in pos_dict:
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []
        if rating >= score_thr:
            pos_dict[userid].append((itemid,1))
        else:
            score = score_dict.get(itemid,0)
            neg_dict[userid].append((itemid, score))
    fp.close()
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num>0:
            train_data += [(userid, co[0], co[1]) for co in pos_dict[userid]][:data_num]
        else:
            continue
        # 对负样本按照平均评分进行排序，element是[itemid,score]，这里表示用户如果对热门的商品评分不高，则很大可能这个用户对这个物品真的没有兴趣
        sorted_neg_list = sorted(neg_dict[userid], key=lambda  element:element[1], reverse=True)[:data_num]
        train_data += [(userid, co[0], 0) for co in sorted_neg_list]
    return train_data

if __name__ == '__main__':
    # item_dict = get_item_info("../data/movies.csv")
    # print(len(item_dict))
    # print(item_dict["1"])
    # print(item_dict["11"])
    #
    # score_dict = get_ave_score("../data/ratings.csv")
    # print(len(score_dict))
    # print(score_dict["31"])

    # train_data = get_train_data("../data/ratings.csv")
    # print(len(train_data))
    # print(train_data[:233])

    pass


