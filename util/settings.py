# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 10:04
# @Author  : Wang Lei
# @FileName: settings.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import os
"""
Settings for PatentCrawler
"""
# ROOT
ROOT = os.path.dirname(os.path.dirname(__file__))

# SOURCE
# SOURCE = os.path.join(ROOT, 'source')
SOURCE = '/home/wanglei/data/'

# util
UTIL = os.path.join(ROOT, 'util')

# 数据库路径
DISTINCT_DB = os.path.join(UTIL, "distinct_db.db")

# 专利全文， 未分词
PATENTS = os.path.join(SOURCE, 'patents')

# 权利要求
CLAIMS = os.path.join(SOURCE, 'claims')

# 中间处理文件
TEMP_DATA = os.path.join(ROOT, "temp_data")

# 分词后的专利全文
TEMP_PATENTS = os.path.join(TEMP_DATA, 'patents')

# 分词后的权利要求
TEMP_CLAIMS = os.path.join(TEMP_DATA, 'claims')

# CRFPOSModelPath
CRFPOSModelPath = "D:/javaworkspace/HanLP-1.6.1/data/model/crf/pku199801/pos.bin"
CRFNERModelPath = "D:/javaworkspace/HanLP-1.6.1/data/model/crf/pku199801/ner.bin"
CRFCWSModelPath = "D:/javaworkspace/HanLP-1.6.1/data/model/crf/pku199801/cws.bin"

# models
MODELS = os.path.join(ROOT, 'models')

WORD2VEC = os.path.join(MODELS, 'word2vec')

# patent term dict about 45227 phrases
TERM_DICT = '/home/wanglei/data/merge_term_dict.txt'

