# -*-coding:utf8-*-
"""
author: fivelike
date: 2021.5.31
"""
import os

def get_user_click(rating_file):
    """
    get user click list
    :param rating_file: input file
    :return: a dict key:userid, value:[itemid1,itemid2,...]
    """
    if not os.path.exists(rating_file):
        return {}, {}
    linenum = 0
    user_click = {}
    user_click_time = {}
    fp = open(rating_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        [userid, itemid, rating, timestamp] = item
        if userid + "_" + itemid not in user_click_time:
            user_click_time[userid + "_" + itemid] = int(timestamp)
        if float(rating) < 3.0:
            continue
        if userid not in user_click:
            user_click[userid] = []
        user_click[userid].append(itemid)
    fp.close()
    return user_click, user_click_time


def get_item_info(item_file):
    """
    get item info[title, genres]
    :param item_file: input file
    :return: a dict: key itemid, value [title, genres]
    """
    if not os.path.exists(item_file):
        return {}
    linenum = 0
    item_info = {}
    fp = open(item_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 3:
            continue
        if len(item) == 3:
            [itemid, title, genres] = item
        elif len(item) > 3:
            itemid = item[0]
            genres = item[-1]
            title = ",".join(item[1:-1])
        if itemid not in item_info:
            item_info[itemid] = [title, genres]
    fp.close()
    return item_info

# if __name__ == '__main__':
# user_click = get_user_click("../data/ratings.csv")
# print(len(user_click))
# print(user_click["1"])
# item_info = get_item_info("../data/movies.csv")
# print(len(item_info))
# print(item_info["1"])
