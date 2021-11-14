from selenium.webdriver.common.by import By


class LoginElement:
    username_textbox = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[1]/div/div[1]/input')
    pwd_textbox = (By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/div/div[1]/input')
    login_btn = (By.CLASS_NAME, 'el-button--primary')
    error_userInfo = (By.XPATH, '//*[contains(text(), "无法使用提供的认证信息登录")]')
    empty_username = (By.XPATH, '//*[contains(text(), "请输入登录名称")]')
    empty_password = (By.XPATH, '//*[contains(text(), "请输入登录密码")]')
    reset_user_info = ('xpath', '//*[@id="app"]/div[1]/div/form/div[3]/div/button[2]/span')
