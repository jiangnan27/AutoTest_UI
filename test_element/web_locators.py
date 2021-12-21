from selenium.webdriver.common.by import By


# 格式说明
# 类名: 页面元素所属模块
# 属性名: 具体元素
# 属性值: ('元素名字', '定位方式', '元素值', （'元素值引用的 {} 数据1', 元素值引用的 {} 数据2）)
# 例子: 原本的 - ('输入框 - 用户名', By.XPATH, '//*[@id="app"]/div[1]/div/form/div[1]/div/div[1]/input', ())
#      也可以 = ('输入框 - 用户名', By.XPATH, '//*[@id="app"]/div[1]/div/form/div[1]/div/div[1]/input')
#      引用的 - ('输入框 - 用户名', By.XPATH, '//*[@id="app"]{}/input', ('/div[1]/div/form/div[1]/div/div[1]',))


class LoginElement:
    username_textbox = ('输入框 - 用户名', By.XPATH, '//*[@id="app"]/div[1]/div/form/div[1]/div/div[1]/input', ())
    pwd_textbox = ('输入框 - 密码', By.XPATH, '//*[@id="app"]/div[1]/div/form/div[2]/div/div[1]/input', ())
    login_btn = ('按钮 - 登录', By.CLASS_NAME, 'el-button--primary', ())
    error_userInfo = ('警告语 - 登录失败', By.XPATH, '//*[contains(text(), "无法使用提供的认证信息登录")]', ())
    empty_username = ('提示语 - 请输入登录名称', By.XPATH, '//*[contains(text(), "请输入登录名称")]', ())
    empty_password = ('提示语 - 请输入密码', By.XPATH, '//*[contains(text(), "请输入登录密码")]', ())
    reset_user_info = ('按钮 - 重置用户信息', 'xpath', '//*[@id="app"]/div[1]/div/form/div[3]/div/button[2]/span', ())
