#! /usr/bin/python
import warnings
from selenium import webdriver
from appium import webdriver as app_driver
from utils.my_logger import log
import json


def get_h5_driver():
    mobile_emulation = {"deviceName": "iPhone 5/SE"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option('w3c', False)
    warnings.simplefilter("ignore", ResourceWarning)
    log.info('打开H5浏览器。')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_web_driver():
    log.info('打开web浏览器。')
    driver = webdriver.Chrome()
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
