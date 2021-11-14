#!/usr/bin/env python
# coding=utf-8
from test_object.app_homePages import HomePages
import pytest


@pytest.mark.usefixtures("app_setup")
@pytest.mark.usefixtures("case_setup")
class TestBrush:

    # @pytest.mark.parametrize("data", ND.notice_data)
    def test_notice_fail(self, app_setup):
        driver = app_setup[0]
        np = HomePages(driver)
        # log432.info('用例名称：{}'.format(data['case_name']))
        while True:
            np.sleep(5)
            np.swipe_for('up')


if __name__ == "__main__":
    pytest.main(['-s', '-q', '--tb=no'])
