"""
处理所有函数的测试类
"""
import os
import sys
# 跳到src目录下
sys.path.append("..")
import unittest
from preprocessing import PreprocessingPatents
from pyhlp import HanLPAPI
from settings import CLAIMS, TEMP_PATENTS

@unittest.skip("TestStringMethods")
class TestStringMethods(unittest.TestCase):
    @unittest.skip("skip is upper")
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


class TestPreprocessingPatents(unittest.TestCase):
    @unittest.skip('')
    def test_init(self):
        print(PreprocessingPatents.__doc__)

    @unittest.skip("test_format_patents skip")
    def test_format_patents(self):
        database = 'F:\\workpace\\PycharmProjects\\PatentCrawler\\util\\distinct_db.db'
        text_dir = 'patents'
        pp = PreprocessingPatents()
        pp.format_patents(database, text_dir)

    @unittest.skip('')
    def test_extra_claims(self):
        database = 'F:\\workpace\\PycharmProjects\\PatentCrawler\\util\\distinct_db.db'
        text_dir = 'claims'
        pp = PreprocessingPatents()
        pp.format_claims(database, text_dir)

    def test_segment_patent_from_sqlite(self):
        pp = PreprocessingPatents()
        pp.segment_patent_from_sqlite()

@unittest.skip('')
class TestHanLPAPI(unittest.TestCase):
    def test_hanlpapi(self):
        hanlpapi = HanLPAPI()
        claim = os.path.join(CLAIMS, "CN00105541.020011003FM_claim.txt")
        with open(claim, "r", encoding='utf-8') as f:
            for line in f.read().split('\n'):
                print(hanlpapi.crf_segment_py(line, False))



        # document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
        #            "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
        #            "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
        #            "严格地进行水资源论证和取水许可的批准。"
        # print(hanlpapi.extract_keyword_py(document, 3))
        # # 自动摘要
        # print(hanlpapi.extract_summary_py(document, 4))
        # # 依存句法分析
        # print(hanlpapi.parse_dependency_py("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))


if __name__ == '__main__':
    unittest.main()


