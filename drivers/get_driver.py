#! /usr/bin/python
import sys
import warnings
from selenium import webdriver
from appium import webdriver as app_driver
import json
from utils.my_logger import log
from config.get_config_data import get_sys_yml_data
from config.PATH import os, DRIVERS


def __get_driver_path(driver_type):
    """
    获取 driver 文件路径
    :param driver_type: 传入 driver 类型, 系统自动 配合 系统配置文件中的文件名, 匹配项目中是否存储有 driver 文件
    :return 有的话，返回 绝对路径
            无的话，返回 None
    """

    driver_type = driver_type.lower()
    if driver_type not in ['chrome', 'firefox', 'ie', 'safari']:
        raise Exception(f'不支持的 driver 类型: {driver_type}')

    current_sys_type = sys.platform
    sys_yml_data = get_sys_yml_data()

    if current_sys_type == 'win32':
        current_sys_type = 'win'
    else:
        current_sys_type = current_sys_type

    driver_name = sys_yml_data['driver_path'][current_sys_type][driver_type]
    if driver_name:
        if os.path.exists(driver_name):  # 如果是 绝对路径的
            driver_path = driver_name
        else:  # 如果是 名字 + driver存放于项目中
            driver_path = os.path.join(DRIVERS, current_sys_type, driver_name)

        if os.path.exists(driver_path):
            return driver_path
        else:
            return None
    else:
        return None


def get_h5_driver(driver_type='chrome'):
    driver_type = driver_type.lower()
    driver_path = __get_driver_path(driver_type)
    if driver_path is None:
        driver_path = 'default_path'

    mobile_emulation = {"deviceName": "iPhone 5/SE"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option('w3c', False)
    warnings.simplefilter("ignore", ResourceWarning)

    log.info(f'driver路径: {driver_path}')
    log.info('打开H5浏览器。')
    if driver_path:
        driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    driver = __check_webdriver_to_undefined(driver)
    return driver


def get_web_driver(driver_type='chrome'):
    driver_type = driver_type.lower()
    driver_path = __get_driver_path(driver_type)
    if driver_path is None:
        driver_path = 'default_path'

    log.info(f'driver路径: {driver_path}')
    log.info('打开web浏览器。')
    if driver_path:
        driver = webdriver.Chrome(executable_path=driver_path)
    else:
        driver = webdriver.Chrome()
    driver = __check_webdriver_to_undefined(driver)
    driver.maximize_window()
    return driver


def get_app_driver(appium_port, desired_caps):
    """
    打开APP
    :param appium_port: appium端口号
    :param desired_caps: 移动设备的关键信息
    """
    log.info('=' * 40 + '  设备初始化信息  ' + '=' * 40)
    log.info('appium_port：{}'.format(appium_port))
    log.info('desired_capabilities：{}'.format(json.dumps(desired_caps, indent=2, ensure_ascii=False)))
    log.info('=' * 40 + '  设备初始化信息  ' + '=' * 40)
    log.info('打开APP。')
    driver = app_driver.Remote(command_executor='http://127.0.0.1:{}/wd/hub'.format(appium_port),
                               desired_capabilities=desired_caps)
    return driver


def __check_webdriver_to_undefined(driver):
    """
    去掉 selenium 反爬检测
    :param driver: driver
    :return: driver
    """
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return driver
