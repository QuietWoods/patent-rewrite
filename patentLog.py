# -*- coding: utf-8 -*-
# @Time    : 2018/5/6 10:33
# @Author  : zoulc001  来源： http://zoulc001.iteye.com/blog/1235878
# @FileName: patentLog.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import logging.handlers
import os

# 日志文件的路径，FileHandler不能创建目录，这里先检查目录是否存在，不存在创建它
# 当然也可以继承之后重写FileHandler的构造函数
src_dir = os.path.dirname(__file__)
LOG_FILE_PATH = os.path.join(src_dir, "log/Execution.log")
dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.isdir(dir):
    os.mkdir(dir)
# 写入文件的日志等级，由于是详细信息，推荐设为debug
FILE_LOG_LEVEL = "DEBUG"
# 控制台的日志等级，info和warning都可以，可以按实际要求定制
CONSOLE_LOG_LEVEL = "INFO"
# 缓存日志等级，最好设为error或者critical
MEMORY_LOG_LEVEL = "ERROR"
# 致命错误等级
URGENT_LOG_LEVEL = "CRITICAL"
# 缓存溢出后的邮件标题
ERROR_THRESHOLD_ACHEIVED_MAIL_SUBJECT = "Too many errors occurred during the execution"
# 缓存溢出的阀值
ERROR_MESSAGE_THRESHOLD = 50
# 致命错误发生后的邮件标题
CRITICAL_ERROR_ACHEIVED_MAIL_SUBJECT = "Fatal error occurred"

# 邮件服务器配置
my_sender = '1258481281@qq.com' # 发件人邮箱账号
my_pass = '*****************'    # 发件人邮箱密码,授权码代替
my_user = 'wanglei_nlp@126.com' # 收件人邮件账号

MAIL_HOST = "smtp.qq.com"
FROM = my_sender
MAIL_TO = ["1258481281@qq.com"]


class OptmizedMemoryHandler(logging.handlers.MemoryHandler):
    """
       由于自带的MemoryHandler达到阀值后，每一条缓存信息会单独处理一次，这样如果阀值设的100，
      会发出100封邮件，这不是我们希望看到的，所以这里重写了memoryHandler的2个方法，
      当达到阀值后，把缓存的错误信息通过一封邮件发出去.
    """

    def __init__(self, capacity, mail_subject):
        logging.handlers.MemoryHandler.__init__(self, capacity, flushLevel=logging.ERROR, target=None)
        self.mail_subject = mail_subject
        self.flushed_buffers = []

    def shouldFlush(self, record):
        """
        检查是否溢出
        """
        if len(self.buffer) >= self.capacity:
            return True
        else:
            return False

    def flush(self):
        """
         缓存溢出时的操作，
        1.发送邮件 2.清空缓存 3.把溢出的缓存存到另一个列表中，方便程序结束的时候读取所有错误并生成报告
        """
        if self.buffer != [] and len(self.buffer) >= self.capacity:
            content = ""
            for record in self.buffer:
                message = record.getMessage()
                level = record.levelname
                ctime = record.created
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
                content += t + " " + "*" + level + "* : " + message + "\n"
            self.mailNotification(self.mail_subject, content)
            self.flushed_buffers.extend(self.buffer)
            self.buffer = []

    def mailNotification(self, subject, content):
        """
                发邮件的方法
        """
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = formataddr([FROM, my_sender])  # 发送者
        msg['To'] = formataddr(['Testing', my_user])  # 接收者
        try:
            smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)    # 发件人邮箱中的SMTP服务器，端口号是25
            smtpObj.login(my_sender, my_pass)
            smtpObj.sendmail(my_sender, [my_user, ], msg.as_string())
            smtpObj.quit()  # 关闭连接
            logging.info('email send successfully')
        except Exception as e:
            self.handleError(e)


MAPPING = {"CRITICAL": 50,
           "ERROR": 40,
           "WARNING": 30,
           "INFO": 20,
           "DEBUG": 10,
           "NOTSET": 0,
           }


class Logger:
    """
    Logger的配置
    """

    def __init__(self, logfile, file_level, console_level, memory_level, urgent_level):

        self.config(logfile, file_level, console_level, memory_level, urgent_level)

    def config(self, logfile, file_level, console_level, memory_level, urgent_level):
        # 生成root logger
        self.logger = logging.getLogger("PatentRewrite")
        self.logger.setLevel(MAPPING[file_level])
        # 生成RotatingFileHandler，设置文件大小为10M,编码为utf-8，最大文件个数为100个，如果日志文件超过100，则会覆盖最早的日志
        self.fh = logging.handlers.RotatingFileHandler(logfile, mode='a', maxBytes=1024 * 1024 * 10, backupCount=100,
                                                       encoding="utf-8")
        self.fh.setLevel(MAPPING[file_level])
        # 生成StreamHandler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(MAPPING[console_level])
        # 生成优化过的MemoryHandler,ERROR_MESSAGE_THRESHOLD是错误日志条数的阀值
        self.mh = OptmizedMemoryHandler(ERROR_MESSAGE_THRESHOLD, ERROR_THRESHOLD_ACHEIVED_MAIL_SUBJECT)
        self.mh.setLevel(MAPPING[memory_level])
        # 生成SMTPHandler
        self.sh = logging.handlers.SMTPHandler(MAIL_HOST, FROM, ";".join(MAIL_TO), CRITICAL_ERROR_ACHEIVED_MAIL_SUBJECT,[my_sender, my_pass])
        self.sh.setLevel(MAPPING[urgent_level])
        # 设置格式
        formatter = logging.Formatter("%(asctime)s %(filename)s  %(lineno)d %(levelname)s : %(message)s", '%Y-%m-%d %H:%M:%S')
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)
        self.mh.setFormatter(formatter)
        self.sh.setFormatter(formatter)
        # 把所有的handler添加到root logger中
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.mh)
        self.logger.addHandler(self.sh)

    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)


LOG = Logger(LOG_FILE_PATH, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL, MEMORY_LOG_LEVEL, URGENT_LOG_LEVEL)
if __name__ == "__main__":
    # 测试代码
    for i in range(50):
        LOG.error(i)
        LOG.debug(i)
    LOG.critical("Database has gone away")
