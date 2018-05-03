
from jpype import *
from PatentCrawler.util.settings import CRFPOSModelPath, CRFCWSModelPath, CRFNERModelPath

class HanLPAPI:
    """
    HanLP Java 工具包的调用接口
    """
    HanLP = None

    def __init__(self):
        """
        类的初始化，启动JVM
        """
        startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\\javaworkspace\\HanLP-1.6.1\\hanlp-1.6.3.jar;"
                                      "D:\\javaworkspace\\HanLP-1.6.1", "-Xms1g",
                 "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
        self.HanLP = JClass('com.hankcs.hanlp.HanLP')
        print("启动JVM:hanlp-1.6.1.jar")

    def __del__(self):
        """
        对象销毁，关闭JVM
        :return:
        """
        shutdownJVM()
        print("关闭JVM")

    def segment_py(self, sentence):
        """
        分词
        :return:
        """
        # 中文分词
        if sentence:
            return self.HanLP.segment(sentence)
        else:
            return None

    def crf_segment_py(self, sentence, pos_mark):
        """
        CRF词法分析器（中文分词、词性标注和命名实体识别）
        :param sentence:
        :return:
        """
        # CRFSegment = JClass("com.hankcs.hanlp.model.crf.CRFSegmenter")
        # crf_seg = CRFSegment(CRFCWSModelPath)
        # CRFPOSTagger = JClass("com.hankcs.hanlp.model.crf.CRFPOSTagger")
        # crf_pos = CRFPOSTagger(CRFPOSModelPath)
        # CRFNERecognizer = JClass("com.hankcs.hanlp.model.crf.CRFNERecognizer")
        # crf_ner = CRFNERecognizer(CRFNERModelPath)
        CRFAnalyzer = JClass("com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer")
        # crf_ana = CRFAnalyzer(crf_seg, crf_pos, crf_ner)
        crf_ana = CRFAnalyzer()
        if sentence and pos_mark:
            return crf_ana.seg(sentence)
        elif sentence:
            return crf_ana.segment(sentence)
        else:
            return None

    def Tokenizer_py(self, sentence):
        """
        命名实体识别与词性标注
        :return:
        """
        # 命名实体识别与词性标注
        NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
        if sentence:
            return NLPTokenizer.segment(sentence)
        else:
            return None

    def extract_keyword_py(self, document, number):
        """
        关键词提取
        :param document:
        :param number: 抽取的关键字数目
        :return:
        """
        # 关键词提取
        if not number:
            number = 2
        if document:
            return self.HanLP.extractKeyword(document, number)
        else:
            return None

    def extract_summary_py(self, document, number):
        """
        自动摘要
        :param document:
        :param number: 抽取的摘要条数
        :return:
        """
        # 自动摘要
        if not number:
            number = 3
        if document:
            return self.HanLP.extractSummary(document, number)
        else:
            return None

    def parse_dependency_py(self, sentence):
        """
        依存句法分析
        :param sentence:
        :return:
        """
        # 依存句法分析
        if sentence:
            return self.HanLP.parseDependency(sentence)
        else:
            return None
