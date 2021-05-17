#-*-coding:utf8-*-
"""
author: fivelike
date: 2021.5.17
personal rank main algo
"""
from tqdm import tqdm
import operator
import sys
sys.path.append("../util")
import util.read as read
def personal_rank(graph, root, alpha, iter_num, recom_num = 10):
    """
    非矩阵化实现 personal rank 算法
    :param graph: user item graph
    :param root: the fixed user for who to recom
    :param alpha: the prob to go to random walk
    :param iter_num: iteration num
    :param recom_num: recom item num
    :return:
        a dict: key itemid, value pr
    """
    rank = {point: 0 for point in graph}
    rank[root] = 1
    recom_result = {}
    for iter_index in tqdm(range(iter_num)):
        tmp_rank = {point: 0 for point in graph}
        for out_point, out_dict in graph.items():
            for inner_point, value in graph[out_point].items():
                tmp_rank[inner_point] += round(alpha*rank[out_point]/len(out_dict),4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1-alpha,4)
        if tmp_rank == rank:
            break
        rank = tmp_rank
    right_num = 0
    for co in sorted(rank.items(), key = operator.itemgetter(1),reverse=True):
        point, pr_score = co[0], co[1]
        if len(point.split('_'))<2:
            continue
        if point in graph[root]:
            continue
        recom_result[point] = pr_score
        right_num +=1
        if right_num > recom_num:
            break
    return recom_result

def get_one_user_recom():
    """
    give one fix_user recom result
    """
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data("../data/ratings.csv")
    iter_num = 100
    recom_result = personal_rank(graph,user,alpha,iter_num)
    """
    # 将推荐结果直接存盘或写入到KV中
    item_info = read.get_item_info("../data/movies.csv")
    for itemid in graph[user]:
        pure_itemid = itemid.split("_")[1]
        print(item_info[pure_itemid])
    print("result---------")
    for itemid in recom_result:
        pure_itemid = itemid.split("_")[1]
        print(item_info[pure_itemid])
        print(recom_result[itemid])
    """

if __name__ == '__main__':
    get_one_user_recom()

