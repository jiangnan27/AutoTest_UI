from test_element.web_locators import LoginElement as LE
from core.pom import UIBasePages


class LoginPages(UIBasePages):

    def input_user_info(self, phone, password):
        self.input_content(LE.username_textbox, phone, 1)
        self.input_content(LE.pwd_textbox, password, 1)

    def click_logbtn(self):
        self.click_ele(LE.login_btn)

    def check_login(self, locator):
        return self.find_ele(locator, 1)

    def reset_user_info(self):
        self.click_ele(LE.reset_user_info)
