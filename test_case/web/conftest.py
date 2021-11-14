#! /usr/bin/python
import pytest
from test_object.web_common_pages import LoginPages
from utils.my_logger import log
from drivers.get_driver import get_web_driver
from config.get_config_data import get_web_yml_data

yaml_data = get_web_yml_data()
url = yaml_data["URL"]["test"]


@pytest.fixture(scope='class')
def browser_setup():
    driver = get_web_driver()
    lg = LoginPages(driver)
    lg.open_url(url)

    # 分割线：上面是setup，下面是teardown
    # 分割线（固定写法） 跟 返回值
    yield lg

    lg.quit_driver()


@pytest.fixture
def case_setup():
    log.info('')
    log.info('<' * 50 + '   用例开始   ' + '>' * 50)

    yield

    log.info('<' * 50 + '   用例结束   ' + '>' * 50)

