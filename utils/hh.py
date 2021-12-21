import datetime
a = ('输入框 - 用户名', 'By.XPATH', '//*[@id="app"]{}{}/input', ('/div[1]', '/div/form/div[1]/div/div[1]'))
print(a[-1])
c = '//*[@id="app"]{}{}/input'.format(1, 2)
print(c)
b = a[2].format(*a[-1])
print(b)



