import os
import re
import sys
from PatentRewrite.patentLog import LOG
import shutil
from PatentRewrite.util.sqlite_to_txt import SqliteUtil
from PatentRewrite.util.settings import TERM_DICT, PATENTS_DB, TEMP_PATENTS
import sqlite3
import logging
import jieba
# 加载自定义词典
# jieba.load_userdict(TERM_DICT)


class PreprocessingPatents:
    """专利文本预处理"""
    def __init__(self):
        pass

    def __str__(self):
        pass

    @staticmethod
    def write_to_txt(w_obj, content):
        """把内容写到txt文本件中"""
        if not content:
            content = '空'
        if not isinstance(content, (str,)):
            w_obj.write(str(content))
        else:
            w_obj.write(content)
        w_obj.write('\n')

    @staticmethod
    def insert_newline_by_punctuation(string):
        """根据标点符号插入换行符"""
        if not string:
            return None
        # 根据中文句号插入换行符
        insert_newline = string.replace('。', '。\n')
        return insert_newline

    @staticmethod
    def clear_claim(claim_instru):
        """
        清洗权利要求书和说明书，并拆开
        :param claim_instru: 包含html标签的专利权利要求书和说明书
        :return: 专利权利要求书和说明书
        """
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

        return claim[5:], instructions[3:]

    @staticmethod
    def extra_claim(claim_instru):
        """
        抽取，清洗权利要求书
        :param claim_instru: 专利权利要求书和说明书
        :return: 格式化后的权利要求书
        """
        if not claim_instru:
            return None
        split_list = claim_instru.split(u'</div>')
        if len(split_list) < 1:
            return None
        claim = split_list[0]
        # 正则表达式去除有效（无效）的html标签 和 任意空白字符
        dr = re.compile(r'</?[^>]+>', re.S)
        claim = dr.sub('', claim)
        dr = re.compile(r'\s+', re.S)
        claim = dr.sub('', claim)
        return claim[5:]

    def format_patents(self, db, text_dir):
        """
         格式化专利文本
           1、从数据库取出发明名称、摘要、权利要求书、说明书
           2、生成文件名为申请号
        :param db:
        :param text_dir:
        :return:
        """
        # 项目根目录下创建文件夹
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        txt_dir = os.path.join(project_dir, text_dir)
        # 先消除再重新生成
        if os.path.exists(txt_dir):
            shutil.rmtree(txt_dir)  # 删除一个非空目录
        os.mkdir(txt_dir)

        patent_txt_dir = txt_dir

        merge_data = SqliteUtil(db)
        records = merge_data.select()
        exist_sum = 0  # 计算重复的专利文本
        for i, record in enumerate(records):
            fname = record[1] + '.txt'  # 以申请号作为文件名
            pattern = r'[\\/:*?"<>|\r\n\t]'  # 匹配不符合window系统下的文件名字符
            format_fname = re.sub(pattern, '_', fname, count=0, flags=0)  # 消除不符合规范的字符

            if os.path.exists(os.path.join(patent_txt_dir, format_fname)):
                exist_sum += 1
                continue
            else:
                pass
            with open(os.path.join(patent_txt_dir, format_fname), 'w', encoding='utf-8') as w:
                # patent_full_text = {'发明名称': 4, '摘要': 9, '权利要求': 21, '说明书': 22}
                # 发明名称
                self.write_to_txt(w, self.insert_newline_by_punctuation(record[6]))
                # 摘要
                self.write_to_txt(w, self.insert_newline_by_punctuation(record[11]))
                # 清洗专利权利要求书和说明书的标签
                claim, instructions = self.clear_claim(record[23])
                # 权利要求书
                self.write_to_txt(w, self.insert_newline_by_punctuation(claim))
                # 说明书
                self.write_to_txt(w, self.insert_newline_by_punctuation(instructions))
            if i % 1000 == 0:
                print("第%d条记录，写入文件。" % i)
            # break
        print('重复的总数： ', exist_sum)

    def format_claims(self, db, text_dir):
        """
        格式化专利权利要求
           1、从数据库取出权利要求书
           2、生成文件名为申请号
           3、以句号断行
        :param db: 数据库文件路径
        :param text_dir: 生成文件存放目录
        :return: 无
        """
        # 项目根目录下创建文件夹
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        txt_dir = os.path.join(project_dir, text_dir)
        # 先消除再重新生成
        if os.path.exists(txt_dir):
            shutil.rmtree(txt_dir)  # 删除一个非空目录
        os.mkdir(txt_dir)
        patent_txt_dir = txt_dir

        merge_data = SqliteUtil(db)
        records = merge_data.select()
        exist_sum = 0  # 计算重复的专利文本
        for i, record in enumerate(records):
            fname = record[1] + '_claim.txt'  # 以申请号作为文件名
            pattern = r'[\\/:*?"<>|\r\n\t]'  # 匹配不符合window系统下的文件名字符
            format_fname = re.sub(pattern, '_', fname, count=0, flags=0)  # 消除不符合规范的字符

            if os.path.exists(os.path.join(patent_txt_dir, format_fname)):
                exist_sum += 1
                continue
            else:
                pass
            with open(os.path.join(patent_txt_dir, format_fname), 'w', encoding='utf-8') as w:
                # patent_full_text = {'发明名称': 4, '摘要': 9, '权利要求': 21, '说明书': 22}
                # 清洗专利权利要求书和说明书的标签，根据句号插入换行符
                claim = self.insert_newline_by_punctuation(self.extra_claim(record[23]))
                # 权利要求书
                self.write_to_txt(w, claim)
            if i % 1000 == 0:
                print("第%d条记录，写入文件。" % i)
            # break
        print('重复的总数： ', exist_sum)

    def count_sentences(self, sentence):
        """统计文本句子的字符长度"""
        if sentence:
            return

    def segment_patent_from_sqlite(self):
        """
        使用jieba分词，自定义词典
        :return:
        """
        # 连接专利全文数据库
        conn = sqlite3.connect(PATENTS_DB)
        logging.info('Opened database successfully')
        c = conn.cursor()
        cursor = c.execute('SELECT * from patent')
        i = 0
        if not os.path.exists(TEMP_PATENTS):
            os.mkdir(TEMP_PATENTS)
        for row in cursor:
            i += 1
            fname = row[1] + '.txt' # 以专利号为文件名
            with open(os.path.join(TEMP_PATENTS, fname), 'w', encoding='utf-8') as w:
                # 标题
                w.write(' '.join(jieba.cut(row[2])))
                w.write('\n\n')
                # 摘要
                w.write(' '.join(jieba.cut(row[3])).replace('。 ', '。\n'))
                w.write('\n\n')
                # 权利要求
                w.write(' '.join(jieba.cut(row[4])).replace('。 ', '。\n'))
                w.write('\n\n')
                # 说明书
                w.write(' '.join(jieba.cut(row[5])).replace('。 ', '。\n'))
            if i >= 10:
                break

    def use_log(self):
        """

        :return:
        """
        i = 1
        LOG.error(i)
        # 测试代码
        for i in range(50):
            LOG.error(i)
            LOG.debug(i)
        LOG.critical("Database has gone away")


if __name__ == "__main__":
    pp = PreprocessingPatents()
    # pp.segment_patent_from_sqlite()
    pp.use_log()

