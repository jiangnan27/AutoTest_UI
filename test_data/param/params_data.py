from test_element.web_locators import LoginElement as LE


class LoginData:
    data = [
        {'username': '', 'password': 'admin123', 'check': LE.empty_username},
        {'username': 'admin123', 'password': '', 'check': LE.empty_password},
        {'username': 'admin2134', 'password': 'admin123', 'check': LE.error_userInfo},
        {'username': 'admin', 'password': 'admin123-+657', 'check': ''}  # 专门的错误用例
    ]
