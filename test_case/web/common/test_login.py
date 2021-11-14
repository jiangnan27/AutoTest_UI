from test_data.param.params_data import LoginData as LD
import pytest
from config.PATH import os, ALLURE_REPORT_RESOURCE, TEST_REPORT
from utils.do_dir import rmdir_next_mkdir, copy_to_dir


@pytest.mark.usefixtures("browser_setup")
@pytest.mark.usefixtures("case_setup")
class TestLogin:

    @pytest.mark.parametrize("data", LD.data)
    def test_login(self, data, browser_setup):
        lg = browser_setup
        lg.reset_user_info()
        lg.input_user_info(data["username"], data["password"])
        lg.click_logbtn()
        result = lg.check_login(data["check"])
        assert result


if __name__ == '__main__':
    """
    --reruns 重试
    -s 显示print内容
    """
    # 这两行仅限本地调试开启，到了jenkins就不要启用了
    rmdir_next_mkdir(ALLURE_REPORT_RESOURCE)  # 清空以前的文件
    # 把history复制过去才能在allure报告中展示“趋势”数据
    copy_to_dir(os.path.join(TEST_REPORT, 'history'), ALLURE_REPORT_RESOURCE)
    # 这两行仅限本地调试开启，到了jenkins就不要启用了
    # '--tb=no',
    pytest.main(['-s', '-q', 'test_login.py', '--tb=no', '--alluredir', ALLURE_REPORT_RESOURCE])  # allure报告源码
    os.system("allure generate {} -c -o {}".format(ALLURE_REPORT_RESOURCE, TEST_REPORT))  # 转化allure报告源码
