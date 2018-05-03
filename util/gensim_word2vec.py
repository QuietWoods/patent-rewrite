# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 11:26
# @Author  : Wang Lei
# @FileName: gensim_word2vec.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import logging
import os
from time import time

import gensim

from .settings import PATENTS
from .pyhlp import HanLPAPI

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 数据准备：每一个句子都是一个分词后的词链表。
class Sentences(object):
    """
    a memory-friendly iterator
    """
    def __init__(self, dirname):
        self.dirname = dirname
        self.hanapi = HanLPAPI()

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), "r", encoding="utf-8"):
                # crf 分词，pos_mark=True 带词性，否则不带词性

                yield self.hanapi.crf_segment_py(line, pos_mark=False)


class Word2vec:
    """
    利用 gensim 的word2vec api 处理词向量
    """
    def __init__(self, model_dir):
        if not model_dir:
            os.mkdir(model_dir)
        self.model_dir = model_dir
        pass

    def train(self):
        """

        :param dirname: 训练语料库
        :return:
        """
        begin = time()
        # 专利全文的目录
        dirname = PATENTS
        sentences = Sentences(dirname=dirname)
        # train word2vec on the sentences
        # default = 1 worker = no parallelization
        model = gensim.models.Word2Vec(sentences, min_count=6, size=200, workers=4)  # default value is 5
        # model.build_vocab(sentences, keep_raw_vocab=True)
        # model.train(sentences)
        model.save(self.model_dir)
        end = time()
        print("Total processing time: %d secondes" %(end - begin))
        print(self.model_dir)

    def evaluating(self, file):
        """
        模型评估：
        评估集：https://raw.githubusercontent.com/RaRe-Technologies/gensim/develop/gensim/test/test_data/questions-words.txt

        :param file: 评估集
        :return:
        """
        model = gensim.models.Word2Vec.load(self.model_dir)
        model.accuracy(file)

    def train_more(self, sentences):
        """
        动态添加训练语料
        :param sentences:
        :return:
        """
        model = gensim.models.Word2Vec.load(self.model_dir)
        model.train(sentences)

