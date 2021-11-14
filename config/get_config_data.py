from utils.do_yaml import YamlHandle
from config.PATH import SYS_YAML, APP_YAML, WEB_YAML


def get_app_yml_data():
    """
    获取 app_yml 数据
    """
    return YamlHandle(APP_YAML).read_data()


def get_sys_yml_data():
    """
    获取 sys_yml 数据
    """
    return YamlHandle(SYS_YAML).read_data()


def get_web_yml_data():
    """
    获取 web_yml 数据
    """
    return YamlHandle(WEB_YAML).read_data()
