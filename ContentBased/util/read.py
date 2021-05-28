# -*-coding:utf8-*-
"""
author: fivelike
date: 2021.5.28
some util function
"""
import os
import operator

def get_ave_score(input_file):
    """
     得到item的平均评分
    :param input_file: user rating file
    :return: a dict, key: itemid value: ave_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record = {}
    ave_score = {}
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record:
            record[itemid] = [0, 0]
        record[itemid][0] += rating
        record[itemid][1] += 1
    fp.close()
    for itemid in record:
        ave_score[itemid] = round(record[itemid][0] / record[itemid][1], 3)
    return ave_score


def get_item_cate(ave_score, input_file):
    """
    获取item的类别，以及每个类别下的所有item，这些item按照score倒排序
    :param ave_score: a dict, key itemid, value rating score
    :param input_file: item info
    :return:
        a dict: key itemid value a dict, key cat value:radio
        a dict: key cate value [itemid1, itemid2, itemid3, ...]
    """
    if not os.path.exists(input_file):
        return {}, {}
    linenum = 0
    topk = 100
    item_cate = {}
    record = {}
    cate_item_sort = {}
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 3:
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split("|")
        ratio = round(1 / len(cate_list), 3)
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio
    fp.close()
    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate] = {}
            itemid_rating_score = ave_score.get(itemid, 0)
            record[cate][itemid] = itemid_rating_score
    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate] = []
        for co in sorted(record[cate].items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            # cate_item_sort[cate].append(co[0]+"_"+str(co[1]))
            cate_item_sort[cate].append(co[0])
    return item_cate, cate_item_sort


def get_latest_timestamp(input_file):
    """
    :param inputfile: user rating file
    only need run once
    """
    if not os.path.exists(input_file):
        return
    linenum = 0
    latest = 0
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        timestamp = int(item[3])
        if timestamp > latest:
            latest = timestamp
    fp.close()
    print(latest)
    # 1537799250


if __name__ == '__main__':
    ave_score = get_ave_score("../data/ratings.csv")
    # print(len(ave_score))
    # print(ave_score["31"])
    item_cate, cate_item_sort = get_item_cate(ave_score, "../data/movies.csv")
    print(item_cate["1"])
    print(cate_item_sort["Children"])
    get_latest_timestamp("../data/ratings.csv")
