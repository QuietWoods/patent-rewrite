# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 11:26
# @Author  : Wang Lei
# @FileName: gensim_word2vec.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
from  PatentRewrite.patentLog import LOG
from PatentRewrite.util.settings import WORD2VEC
import os
from time import time

import gensim

from PatentRewrite.util.settings import TEMP_PATENTS, STOP_WORDS_DICT


# 数据准备：每一个句子占一行，词语用空格分隔。
class Sentences(object):
    """
    a memory-friendly iterator
    """
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        i = 0
        for fname in os.listdir(self.dirname):
            i += 1
            for line in open(os.path.join(self.dirname, fname), "r", encoding="utf-8"):
                newline = line.strip()
                # 过滤段落间的空行
                if newline:
                    # 去除停用词
                    yield self.remove_stop_words(newline)
            if i > 10:
                break

    @staticmethod
    def stop_words_list(filepath):
        """
        创建停用词list
        :return:
        """
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def remove_stop_words(self, sentence):
        """
        对分词后的句子去除停用词
        :param sentence:
        :return:
        """
        stopwords = self.stop_words_list(STOP_WORDS_DICT)  # 这里加载停用词的路径
        out_list = []
        for word in sentence.strip().split(' '):
            if word not in stopwords:
                if word != '\t' and '\n':
                    out_list.append(word)
        return out_list


class Word2vec:
    """
    利用 gensim 的word2vec api 处理词向量
    """
    def __init__(self, model_dir):
        """
        生成模型的目录
        :param model_dir:
        """
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        self.model_dir = model_dir
        pass

    def train(self):
        """
        训练词向量
        :param dirname: 训练语料库
        :return:
        """
        begin = time()
        # 专利全文的目录
        dirname = TEMP_PATENTS
        sentences = Sentences(dirname=dirname)
        # train word2vec on the sentences
        # default = 1 worker = no parallelization
        # sentences = ['word1', word2']
        """
        sentences=None, size=100, alpha=0.025, window=5, min_count=5,
            max_vocab_size=None, sample=1e-3, seed=1, workers=3, min_alpha=0.0001,
            sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=hash, iter=5, null_word=0,
            trim_rule=None, sorted_vocab=1, batch_words=MAX_WORDS_IN_BATCH, compute_loss=False):
        """
        model = gensim.models.Word2Vec(sentences, size=200, window=10, min_count=10, workers=4)
        # model.build_vocab(sentences, keep_raw_vocab=True)
        # model.train(sentences)
        print('---')
        print(self.model_dir)
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


if __name__ == '__main__':

    Word2vec(WORD2VEC).train()


