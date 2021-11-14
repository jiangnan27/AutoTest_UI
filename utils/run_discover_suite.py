import unittest
from HTMLTestRunnerCN import HTMLTestRunner
from core.pom import *
from utils.my_logger import log as log00
from utils.do_dir import path_join
from utils.my_functions import my_get_now, my_get_date


def run_all_suite(cases_dir, report_title):
    """
    跑一个目录下的所有unittest用例
    这个不是pytest的，只是为了支持unittest报告框架
    """
    # 获取系统当前时间
    now = my_get_now()
    day = my_get_date()

    # 定义个报告存放路径，支持相对路径
    report_filepath = path_join(TEST_REPORT, day)

    # # 通过defaultTestLoader来加载当前目录下所有名称为test开头的py
    suite = unittest.defaultTestLoader.discover(cases_dir, pattern='test*.py', top_level_dir=None)

    if os.path.exists(report_filepath):  # 检验文件夹路径是否已经存在
        pass
    else:
        os.mkdir(report_filepath)  # 创建测试报告文件夹

    report_prefix = os.path.split(cases_dir)[1]

    report_filename = path_join(report_filepath, now + '_' + report_prefix + '_result.html')

    fp = open(report_filename, 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title=report_title,
                            description='执行情况：',
                            custom_logger=log00)

    runner.run(suite)
    fp.close()  # 关闭报告文件
