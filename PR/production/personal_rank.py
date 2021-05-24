# -*-coding:utf8-*-
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
import util.mat_util as mat_util
from scipy.sparse.linalg import gmres
import numpy as np


def personal_rank(graph, root, alpha, iter_num, recom_num=10):
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
                tmp_rank[inner_point] += round(alpha * rank[out_point] / len(out_dict), 4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1 - alpha, 4)
        if tmp_rank == rank:
            print('out' + str(iter_index))
            break
        rank = tmp_rank

    right_num = 0
    for co in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
        point, pr_score = co[0], co[1]
        if len(point.split('_')) < 2:
            continue
        if point in graph[root]:
            continue
        recom_result[point] = pr_score
        right_num += 1
        if right_num >= recom_num:
            break
    return recom_result


def personal_rank_matrix(graph, root, alpha, recom_num=10):
    """
    :param graph: user item graph
    :param root: the fix user to recom
    :param alpha: the prob to random walk
    :param recom_num: recom item num
    :return: a dict, key itemid, value pr score
    """
    m, vertex, address_dict = mat_util.graph_to_m(graph)
    if root not in address_dict:
        return {}
    score_dict = {}
    recom_dict = {}

    mat_all = mat_util.mat_all_point(m, vertex, alpha)
    index = address_dict[root]
    initial_list = [[0] for i in range(len(vertex))]
    initial_list[index] = [1]
    r_zero = np.array(initial_list)

    res = gmres(mat_all, r_zero, tol=1e-8)[0]

    for i in range(len(res)):
        point = vertex[i]
        if len(point.strip().split('_')) < 2:
            continue
        if point in graph[root]:
            continue
        score_dict[point] = round(res[i], 3)
    for co in sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:recom_num]:
        point, score = co[0], co[1]
        recom_dict[point] = score
    return recom_dict


def get_one_user_recom():
    """
    give one fix_user recom result
    """
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data("../data/ratings.csv")
    iter_num = 100
    recom_result = personal_rank(graph, user, alpha, iter_num, 100)
    return recom_result
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


def get_one_user_by_mat():
    """
    give one fix user by mat
    """
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data("../data/ratings.csv")
    recom_result = personal_rank_matrix(graph, user, alpha, 100)
    return recom_result


if __name__ == '__main__':
    recom_result_base = get_one_user_recom()
    recom_result_mat = get_one_user_by_mat()
    num = 0
    for i in recom_result_base:
        if i in recom_result_mat:
            # print(i)
            num += 1
    print("迭代版本与矩阵版本top100相同数：", num)
