import getpass
import re
import subprocess
from config.PATH import os, APP_YAML
from config.get_config_data import get_app_yml_data
from utils.do_dir import get_filenames, loop_search_dir
from utils.my_logger import log
from core.pom import UIBasePages
from drivers.get_driver import get_web_driver
from utils.do_yaml import YamlHandle


# 0. 检测 adb 环境信息
def check_adb_env(phone_address):
    log.info(f"检查 adb、aapt: {phone_address}")

    adb_v = os.popen("adb version").read()
    aapt_v = os.popen("aapt version").read()

    if "Installed" in adb_v and ", v" in aapt_v:
        log.info(adb_v)
        log.info(aapt_v)
        adb_devices = os.popen("adb devices").read()
        if phone_address in adb_devices:
            log.info(adb_devices)
            return True
        else:
            raise Exception(f"未连接设备: {adb_devices}")
    else:
        raise Exception(f"adb、aapt 环境有误: \n {adb_v} \n {aapt_v}")


# 1. 打开web浏览器 -> 下载APP
def download_apk(pgy_url):
    log.info(f"下载APP: {pgy_url}")
    driver = get_web_driver()
    web = UIBasePages(driver)
    web.open_url(pgy_url)
    web.click_ele(("按钮 - 安装", 'xpath', '//*[@id="down_load"]'))
    web.sleep(20)
    web.quit_driver()


# 2. 获取 apk 路径
def get_apk_path(test_app_name):
    log.info(f"获取 apk 包路径: {test_app_name}")
    # username = getpass.getuser()
    # username = os.listdir(r"C:\Users")[0]
    # username = loop_search_dir(r'C:\Users', 'Downloads', 2)[0]
    apk_base_path = loop_search_dir(r'C:\Users', 'Downloads', 2)[0]

    apk_name = None
    keywords = get_app_yml_data()[test_app_name]['apk_info']['apk_name_keywords']
    keyword_all_in = False  # 是否全都包含有关键字
    for file in get_filenames(apk_base_path):
        for keyword in keywords:
            if keyword in file:
                keyword_all_in = True
            else:
                keyword_all_in = False
        if keyword_all_in is True:
            apk_name = file
            break
    if keyword_all_in is False:
        raise Exception(f'没有您想要的APP: {keywords}')
    else:
        apk_path = os.path.join(apk_base_path, apk_name)
        return apk_path


# 2. 获取下载APP的信息
def get_apk_info(apk_path):
    log.info(f"获取 新 apk 的信息: {apk_path}")
    # apk_path = r"C:\Users\23983\Downloads\53伴学测试版_2.01.03.apk"
    cmd = f"aapt dump badging {apk_path}"

    stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    need_out = [i for i in stdout.decode('ISO-8859-1').split('\n') if "package: " in i or "-activity: " in i]
    package_name = re.findall(r'(?<=name=\').*?(?=\')', need_out[0])[0]
    package_version = re.findall(r'(?<=versionName=\').*?(?=\')', need_out[0])[0]
    activity_name = re.findall(r'(?<=name=\').*?(?=\')', need_out[1])[0]
    return {
        "apk_path": apk_path,
        "package_name": package_name,
        "package_version": package_version,
        "activity_name": activity_name
    }


# 4. 获取 手机信息 和 已安装的APP信息
def get_phone_info(phone_address):
    log.info(f"获取手机信息: {phone_address}")
    cmd = f"adb -s {phone_address} shell getprop ro.build.version.release"
    phone_version = os.popen(cmd).read().replace("\n", "").replace(" ", "")
    return {
        "phone_version": phone_version
    }


# 获取 已安装APP 的信息
def get_installed_app_info(phone_address, package_info):
    cmd = f'adb -s {phone_address} shell dumpsys package {package_info["package_name"]} | findstr "versionName"'
    # stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # installed_package_versionName = stdout.split('=')[-1]
    installed_package_version_name = os.popen(cmd).read().replace("\n", "").split("=")[-1]
    return {
        "installed_package_version": installed_package_version_name
    }


# 检查是否安装 apk 包
def check_is_installed_apk(phone_address, apk_info):
    log.info(f'检查 是否安装: {apk_info["package_name"]}')
    installed_list_cmd = f'adb -s {phone_address} shell pm list package -3'
    log.info(installed_list_cmd)
    installed_list_res = os.popen(installed_list_cmd).read()
    if apk_info["package_name"] in installed_list_res:
        log.info(installed_list_res)
        return True
    else:
        return False


# 卸载APP
def uninstall_apk(phone_address, apk_info):
    if check_is_installed_apk(phone_address, apk_info):
        log.info(f'卸载 APP: {apk_info["package_name"]}')
        uninstall_cmd = f'adb -s {phone_address} uninstall {apk_info["package_name"]}'
        log.info(uninstall_cmd)
        uninstall_res = os.popen(uninstall_cmd).read()
        if "Success" in uninstall_res or f'Unknown package' in uninstall_res:
            log.info(uninstall_res)
        else:
            raise Exception(f'apk 卸载失败: {uninstall_res}')


# 4. 安装APP
def install_apk(phone_address, apk_info):
    uninstall_apk(phone_address, apk_info)

    log.info(f'安装 apk: ')
    install_cmd = f'adb -s {phone_address} install {apk_info["apk_path"]}'
    log.info(install_cmd)
    install_res = os.popen(install_cmd).read()
    if "Success" in install_res:
        log.info(install_res)
    else:
        raise Exception(f'apk 安装失败: {install_res}')


# 初始化 APP 环境
def init_apk_env(test_app_name):
    log.info(f"安装APP: {test_app_name}")
    phone_address = get_app_yml_data()[test_app_name]["apk_info"]["phone_address"]
    pgy_url = get_app_yml_data()[test_app_name]["apk_info"]["pgy_url"]

    # 1. 检查 adb 环境
    check_adb_env(phone_address)

    # 2. 下载 apk
    download_apk(pgy_url)

    new_apk_path = ''

    try:
        # 3. 获取下载 app 的 路径
        new_apk_path = get_apk_path(test_app_name)

        # 4. 获取 新 apk 包的信息
        new_apk_info = get_apk_info(new_apk_path)

        # 5. 获取 已安装的包的信息
        installed_package = get_installed_app_info(phone_address, new_apk_info)

        log.info(f'APP: {installed_package["installed_package_version"]} -> {new_apk_info["package_version"]}')

        if installed_package["installed_package_version"] != new_apk_info["package_version"]:
            install_apk(phone_address, new_apk_info)

            old_app_yml_data = get_app_yml_data()
            phone_info = get_phone_info(phone_address)
            new_desired_caps = {
                "automationName": "UIAutomator2",
                "platformName": "Android",
                "platformVersion": phone_info["phone_version"],
                "devicesName": "Android Emulator",
                "noReset": False,
                "appPackage": new_apk_info["package_name"],
                "appActivity": new_apk_info["activity_name"]
            }
            old_app_yml_data[test_app_name]["desired_caps"].update(new_desired_caps)

            YamlHandle(APP_YAML).write_data(old_app_yml_data)

        else:
            log.info("包版本相同，退出安装")
    except Exception as e:
        raise e
    finally:
        # 删除 本地 apk
        log.info(f"删除本地 apk 包: {new_apk_path}")
        os.remove(new_apk_path)

# check_adb_env()
# print(get_apk_path("53banxue"))
# print(get_apk_info(get_apk_path("53banxue")))
# print(get_installed_app_info(get_apk_info(get_apk_path("53banxue"))))
# print(install_apk("53banxue"))


init_apk_env("53banxue")

