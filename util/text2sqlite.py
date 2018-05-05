# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 15:28
# @Author  : Wang Lei
# @FileName: text2sqlite.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import os
import sqlite3
from PatentCrawler.util.settings import PATENTS_TEXT


def text2sqlite(text_dir, database):
    """把文本存储到sqlite数据库中
       文本格式：专利标题，摘要，权利要求，说明书各占一行。
       格式化字段：专利号，标题，摘要，权利要求，说明书。
    """
    # 连接数据库文件，如果不存在则创建
    conn = sqlite3.connect(database)
    print("成功打开数据库文件！")
    c = conn.cursor()
    # c.execute('''CREATE TABLE patent
    #        (ID INT PRIMARY KEY    NOT NULL,
    #        NUMBER  TEXT    NOT NULL,
    #        NAME        TEXT     NOT NULL,
    #        ABSTRACT    TEXT NOT NULL,
    #        CLAIM       TEXT NOT NULL,
    #        INSTRUCTION TEXT NOT NULL);
    #        ''')
    # c.execute('''CREATE UNIQUE INDEX PATENT_NUMBER
    #         on patent (NUMBER);''')
    print("表格创建成功")
    # conn.commit()
    # conn.close()
    # 遍历目录
    temp_data = []
    i = 0
    for item, fname in enumerate(os.listdir(text_dir)):
        temp_data.append(item+1)
        patent_num = fname.split("_")[-1].strip(".txt")
        # 专利号
        temp_data.append(patent_num)
        for num, line in enumerate(open(os.path.join(text_dir, fname), encoding='utf-8')):
            # 发明名称 ，摘要， 权利要求， 说明书
            if num >= 24:
                temp_data.append(line.strip().split('\t')[1])
        # print(temp_data)
        c.execute('INSERT INTO patent VALUES (?, ?, ?, ?, ?, ?)', temp_data)

        print("-----------------------")
        # print(temp_data)
        temp_data = []
        i += 1
        # if i == 10:
        #     break
        print(i)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    text2sqlite(PATENTS_TEXT, 'patents.db')
