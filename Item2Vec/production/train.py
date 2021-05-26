# -*-coding:utf8-*-
"""
author: fivelike
date: 2021.5.26
train word2vec
"""

from gensim.models import word2vec

if __name__ == '__main__':
    sentences = word2vec.LineSentence("../data/train_data.txt")
    model = word2vec.Word2Vec(sentences, sg=1, vector_size=128, window=5, sample=1e-3, hs=0, negative=5, epochs=100)
    model.wv.save_word2vec_format("../data/item_vec.txt", binary=False)
