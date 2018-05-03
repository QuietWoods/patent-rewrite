# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 9:58
# @Author  : wanglei
# @Site    : 
# @File    : sqlite_to_txt.py
# @Software: PyCharm Community Edition
import sqlite3
import os
import re
import sys
from xml.dom.minidom import parse
from xml.dom import minidom

class SqliteUtil:
    'sqlite3 的工具类'
    conn = None
    c = None
    key_dict = {'request_date': '申请日', 'agency': '代理机构', 'invention_type': '发明类型', 'CPC_class_number': 'CPC分类号',
                 'publish_date': '公开（公告）日', 'instructions': '说明书', 'proposer_address': '申请人地址', 'priority_number': '优先权号',
                 'ECLA_class_number': 'ECLA分类号', 'locarno_class_number': '外观设计洛迦诺分类号', 'legal_status': '法律状态',
                 'invention_name': '发明名称', 'publish_country': '公开国', 'legal_status_effective_date': '法律状态生效日期',
                 'claim': '权利要求', 'FI_class_number': 'FI分类号', 'proposer_post_code': '申请人邮编', 'ipc_class_number': 'IPC分类号',
                 'request_number': '申请号', 'UC_class_number': 'UC分类号', 'priority_date': '优先权日', 'publish_number': '公开（公告）号',
                 'abstract': '摘要', 'proposer': '申请（专利权）人', 'proposer_location': '申请人所在国（省）', 'agent': '代理人',
                 'inventor': '发明人', 'FT_class_number': 'FT分类号'}
    keys = ['申请号', '申请日', '公开（公告）号', '公开（公告）日', '发明名称', '申请（专利权）人', '发明人',  '法律状态',  '法律状态生效日期',
            '摘要', 'IPC分类号', '优先权号',  '优先权日', '外观设计洛迦诺分类号',  '代理人', '代理机构', '申请人邮编', '申请人地址',
            '申请人所在国（省）',  '发明类型', '公开国', '权利要求书', '说明书', 'FT分类号', 'UC分类号', 'ECLA分类号', 'FI分类号', 'CPC分类号']

    def __init__(self, database):
        '''init sqlite3 connection'''
        self.conn = sqlite3.connect(database)
        print("Opened database successfully")
        self.c = self.conn.cursor()

    def __del__(self):
        '''close the connection'''
        self.conn.commit()
        self.conn.close()
        class_name = self.__class__.__name__
        print(class_name, "销毁")

    def create(self, sql):
        '''create'''
        if not sql:
            sql = '''CREATE TABLE "patents" ("row_id" INTEGER NULL, "patent_id" VARCHAR(255) NOT NULL,
            "request_number" VARCHAR(255) NOT NULL, "request_date" DATE NOT NULL, "publish_number" VARCHAR(255) NOT NULL,
             "publish_date" DATE NOT NULL, "invention_name" VARCHAR(255) NOT NULL, "proposer" VARCHAR(255) NOT NULL,
             "inventor" VARCHAR(255) NOT NULL, "legal_status" VARCHAR(255), "legal_status_effective_date" DATE,
             "abstract" TEXT, "ipc_class_number" VARCHAR(255), "priority_number" VARCHAR(255), "priority_date" DATE,
             "locarno_class_number" VARCHAR(255), "agent" VARCHAR(255), "agency" VARCHAR(255), "proposer_post_code" VARCHAR(255),
             "proposer_address" VARCHAR(255), "proposer_location" VARCHAR(255), "invention_type" VARCHAR(255), "publish_country" TEXT,
             "claim" TEXT, "instructions" TEXT, "FT_class_number" VARCHAR(255), "UC_class_number" VARCHAR(255),
             "ECLA_class_number" VARCHAR(255), "FI_class_number" VARCHAR(255), "CPC_class_number" VARCHAR(255));'''
        self.c.execute(sql)
        print("Table created successfully")

    def select(self, sql=None):
        '''select'''
        if not sql:
            self.c.execute('SELECT * FROM patents')
        else:
            self.c.execute(sql)
        return self.c.fetchall()

    def insert_one(self, record):
        data = tuple(record[1:])

        result = self.c.execute('INSERT INTO patents(patent_id, request_number, request_date, publish_number, \
                           publish_date, invention_name, proposer, inventor, legal_status, \
                           legal_status_effective_date, abstract, ipc_class_number, priority_number, priority_date,\
                            locarno_class_number, agent,agency, proposer_post_code, proposer_address, \
                           proposer_location,invention_type, publish_country, claim,instructions, \
                           FT_class_number, UC_class_number, ECLA_class_number, FI_class_number,\
                            CPC_class_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                           ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)', data)
        return result


    def insert_many(self, records):
        # Larger example that inserts many records at a time
        records = IterData(records)
        self.c.execute('INSERT INTO patents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                           ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)')
        self.c.executemany('INSERT INTO patents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                           ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)', records.records)
        # self.c.executemany('INSERT INTO patents VALUES ("row_id", "patent_id", "request_number", "request_date", "publish_number", \
        #                    "publish_date", "invention_name", "proposer", "inventor", "legal_status", '
        #                    '"legal_status_effective_date", "abstract", "ipc_class_number", "priority_number", "priority_date",\
        #                     "locarno_class_number", "agent","agency", "proposer_post_code", "proposer_address", \
        #                    "proposer_location","invention_type", "publish_country", "claim","instructions", \
        #                    "FT_class_number", "UC_class_number", "ECLA_class_number", "FI_class_number",\
        #                     "CPC_class_number")', records.records)


class IterData(object):
    '''iterator records'''
    def __init__(self, records):
        self.records = records

    def __iter__(self):
        for record in enumerate(self.records):
            print(record)
            yield record


class db_file(object):
    '''iterator records'''
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for dirpath, dirnames, filenames in os.walk(self.dirname):
            for filename in filenames:
                yield os.path.join(dirpath, filename)


def merge_db(sampe, merge):
    sampe_obj = SqliteUtil(sampe)
    merge_obj = SqliteUtil(merge)
    if not merge_obj.select("SELECT name FROM sqlite_master WHERE type='table';"):
        merge_obj.create(None)
    records = sampe_obj.select(None)
    if records:

        merge_obj.insert_many(records)
    del merge_obj
    del sampe_obj


def distinct_merge_db(sampe, merge):
    sampe_obj = SqliteUtil(sampe)
    merge_obj = SqliteUtil(merge)
    if not merge_obj.select("SELECT name FROM sqlite_master WHERE type='table';"):
        sql = '''CREATE TABLE "patents" ("row_id" INTEGER PRIMARY KEY AUTOINCREMENT, "patent_id" VARCHAR(255) NOT NULL,
                    "request_number" VARCHAR(255) NOT NULL, "request_date" DATE NOT NULL, "publish_number" VARCHAR(255) NOT NULL,
                     "publish_date" DATE NOT NULL, "invention_name" VARCHAR(255) NOT NULL, "proposer" VARCHAR(255) NOT NULL,
                     "inventor" VARCHAR(255) NOT NULL, "legal_status" VARCHAR(255), "legal_status_effective_date" DATE,
                     "abstract" TEXT, "ipc_class_number" VARCHAR(255), "priority_number" VARCHAR(255), "priority_date" DATE,
                     "locarno_class_number" VARCHAR(255), "agent" VARCHAR(255), "agency" VARCHAR(255), "proposer_post_code" VARCHAR(255),
                     "proposer_address" VARCHAR(255), "proposer_location" VARCHAR(255), "invention_type" VARCHAR(255), "publish_country" TEXT,
                     "claim" TEXT, "instructions" TEXT, "FT_class_number" VARCHAR(255), "UC_class_number" VARCHAR(255),
                     "ECLA_class_number" VARCHAR(255), "FI_class_number" VARCHAR(255), "CPC_class_number" VARCHAR(255));'''
        merge_obj.create(sql)
    records = sampe_obj.select(None)
    if records:
        for i, item in enumerate(records):
            sql = "select patent_id from patents where patent_id='%s'" % str(item[1])
            patent_ids = merge_obj.select(sql=sql)
            if i % 100 == 0:
                print('第%d条记录' % i)
            if patent_ids:
                # print('patent_id is exist')
                continue
            else:
                merge_obj.insert_one(item)
    del merge_obj
    del sampe_obj

def merge_dbs():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    patent_db_dir = os.path.join(project_dir, 'output')
    files = db_file(patent_db_dir)
    patents_db_list = []
    for i, item in enumerate(files):
        # print(i, os.path.join(patent_db_dir, item))
        if item.endswith('db'):
            patents_db_list.append(item)

    for k, v in enumerate(patents_db_list):
        merge_db(v, 'merge.db')
        print(k, v)


def list_db_files():
    pass


def write_to_txt(w_obj, key, content):
    w_obj.write(key)
    w_obj.write('\t')
    if not content:
        content = '空'
    if not isinstance(content, (str,)):
        w_obj.write(str(content))
    else:
        w_obj.write(content)
    w_obj.write('\n')


def clear_claim(claim_instru):
    '''清洗权利要求书和说明书，并拆开'''
    if not claim_instru:
        return None, None
    split_list = claim_instru.split(u'</div>')
    if len(split_list) < 2:
        return None, None
    claim, instructions = split_list[0], split_list[1]
    # 正则表达式去除有效（无效）的html标签
    dr = re.compile(r'</?[^>]+>', re.S)
    claim = dr.sub('', claim)
    instructions = dr.sub('', instructions)
    # 去除任意空白字符
    dr = re.compile(r'\s+', re.S)
    claim = dr.sub('', claim)
    instructions = dr.sub('', instructions)
    # print('cliam: ', claim)
    # print('instru: ', instructions)
    return segment_by_punctuation(claim[5:]), segment_by_punctuation(instructions[3:])


# 根据标点符号切割段落
def segment_by_punctuation(string):
    if not string:
        return None
    split_list = string.split(u'。')
    result = ''
    for seg in split_list:
        result += seg + '\n'
    return result


def sqlite_to_txt1(db):
    # project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_dir = "F:\\workpace\\PycharmProjects\\PatentCrawler\\patent50000"
    patent_txt_dir = os.path.join(project_dir, 'txt')
    if os.path.exists(patent_txt_dir):
        pass
    else:
        os.mkdir(patent_txt_dir)
    merge_data = SqliteUtil(db)
    records = merge_data.select()
    for i, record in enumerate(records):
        fname = record[6] + '_' + record[1] + '.txt'
        pattern = r'[\\/:*?"<>|\r\n\t]'
        format_fname = re.sub(pattern, '_', fname, count=0, flags=0)
        with open(os.path.join(patent_txt_dir, format_fname), 'w', encoding='utf-8') as w:
            keys = merge_data.keys
            # patent_full_text = {'发明名称': 4, '摘要': 9, '权利要求': 21, '说明书': 22}
            for k, v in enumerate(keys):
                if k in [4, 9, 21, 22]:
                    continue
                k += 2
                content = record[k]

                write_to_txt(w, v, content)
            # 发明名称
            write_to_txt(w, keys[4], record[6])
            # 摘要
            write_to_txt(w, keys[9], record[11])
            # 清洗专利权利要求书和说明书的标签
            claim, instructions = clear_claim(record[23])
            # 权利要求书
            write_to_txt(w, keys[21], claim)
            # 说明书
            write_to_txt(w, keys[22], instructions)
        if i % 100 == 0:
            print("第%d条记录，写入文件。" % i)
        # break


def sqlite_to_txt(db, text_dir):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txt_dir = os.path.join(project_dir, text_dir)
    if not os.path.exists(txt_dir):
        os.mkdir(txt_dir)
    patent_txt_dir = txt_dir

    merge_data = SqliteUtil(db)
    records = merge_data.select()
    exist_sum = 0
    for i, record in enumerate(records):
        fname = record[6] + '_' + record[1] + '.txt'
        pattern = r'[\\/:*?"<>|\r\n\t]'
        format_fname = re.sub(pattern, '_', fname, count=0, flags=0)

        if os.path.exists(os.path.join(patent_txt_dir, format_fname)):
            # print(i, format_fname, 'exist!')
            exist_sum += 1
            continue
        else:
            print(i, format_fname)
        with open(os.path.join(patent_txt_dir, format_fname), 'w', encoding='utf-8') as w:
            keys = merge_data.keys
            # patent_full_text = {'发明名称': 4, '摘要': 9, '权利要求': 21, '说明书': 22}
            for k, v in enumerate(keys):
                if k in [4, 9, 21, 22]:
                    continue
                k += 2
                content = record[k]

                write_to_txt(w, v, content)
            # 发明名称
            write_to_txt(w, keys[4], record[6])
            # 摘要
            write_to_txt(w, keys[9], segment_by_punctuation(record[11]))
            # 清洗专利权利要求书和说明书的标签
            claim, instructions = clear_claim(record[23])
            # 权利要求书
            write_to_txt(w, keys[21], claim)
            # 说明书
            write_to_txt(w, keys[22], instructions)
        if i % 100 == 0:
            print("第%d条记录，写入文件。" % i)
        # break
    print('存在的总数： ', exist_sum)



if __name__ == '__main__':
    # db1 = 'C:\\Users\\wl\\Downloads\\merge.db'
    # sqlite_to_txt(db1)
    # sampe = 'C:\\Users\\wl\\Downloads\\merge.db'
    # sampe = 'merge.db'
    # distinct_merge_db(sampe, 'distinct_db.db')
   # sqlite_to_txt('distinct_db.db', 'seg_txt')
    print("这是一个中文编码测试！")







