# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 16:52
# @Author  : Wang Lei
# @FileName: tools.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import os
from PatentRewrite.util.gensim_word2vec import Word2vec, Sentences
from PatentRewrite.util.settings import WORD2VEC, PATENTS, TEMP_PATENTS


def train_word2vec():

    model_dir = WORD2VEC
    word2vec = Word2vec(model_dir)
    word2vec.train()


if __name__ == "__main__":

    train_word2vec()
