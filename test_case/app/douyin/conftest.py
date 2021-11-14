import pytest
from drivers.get_driver import get_app_driver
from test_object.app_homePages import HomePages
from utils.my_logger import log
from config.get_config_data import get_app_yml_data


lg = None


@pytest.fixture(scope='class')
def app_setup():
    global lg
    yaml_data = get_app_yml_data()
    appium_port = yaml_data['PRO_APP_DES']['appium_port']
    desired_caps = yaml_data['PRO_APP_DES']['desired_caps']
    driver = get_app_driver(appium_port, desired_caps)
    lg = HomePages(driver)
    # if lg.wait_visibility(LG.md_content, 3):    # 如果有用户协议出现的话，就点击同意（用户协议）
    #     lg.click_element(LG.accept_btn)
    # elif lg.wait_visibility(LG.login_btn, 3):  # 如果有登录按钮在的话就登陆
    #     lg.login(phone, password)

    # 分割线：上面是setup，下面是teardown
    # 分割线（固定写法） 跟 返回值
    yield driver, lg

    lg.quit_driver()


@pytest.fixture
def case_setup():
    log.info('')
    log.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   用例开始   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    yield

    log.info('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   用例结束   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    log.info('')
