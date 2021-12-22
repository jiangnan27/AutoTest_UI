#! /usr/bin/python
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYS_YAML = os.path.join(BASE_PATH, 'config', 'config_sys.yml')
APP_YAML = os.path.join(BASE_PATH, 'config', 'config_app.yml')
WEB_YAML = os.path.join(BASE_PATH, 'config', 'config_web.yml')
CORE = os.path.join(BASE_PATH, 'core')
TEST_ELEMENT = os.path.join(BASE_PATH, 'test_element')
TEST_OBJECT = os.path.join(BASE_PATH, 'test_object')
FILE_DATA = os.path.join(BASE_PATH, 'test_data', 'file_data')
API_BASE_CASE_DATA = os.path.join(BASE_PATH, 'test_data', 'api', 'base_case_data')
API_CSV_CASE_DATA = os.path.join(BASE_PATH, 'test_data', 'api', 'csv_case_data')
UI_CASE_DATA = os.path.join(BASE_PATH, 'test_data', 'ui')
ALLURE_REPORT_RESOURCE = os.path.join(BASE_PATH, 'output', 'allure_report_resource')
TEST_CASE = os.path.join(BASE_PATH, 'test_case')
TEST_LOG = os.path.join(BASE_PATH, 'output', 'test_log')
TEST_REPORT = os.path.join(BASE_PATH, 'output', 'test_report')
TEST_SCREENSHOT = os.path.join(BASE_PATH, 'output', 'test_screenshot')
UTILS = os.path.join(BASE_PATH, 'utils')
DRIVERS = os.path.join(BASE_PATH, 'drivers')
