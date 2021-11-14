from core.pom import APPBasePage
from test_element.app_locators import DouYinHome as DYH


class HomePages(APPBasePage):
    # 进入notice首页
    def into_douyin_home(self):
        self.click_ele(DYH.into_home)  # 进入抖音首页
