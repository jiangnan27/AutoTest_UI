import datetime
import time
# import win32con
# import win32gui
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import TouchActions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from utils.do_yaml import YamlHandle
from config.PATH import *
from utils.my_functions import my_del_symbol
from utils.my_logger import log


class UIBasePages:
    def __init__(self, driver):
        self.driver = driver
        self.touch = TouchActions(self.driver)
        self.chains = ActionChains(self.driver)

    def __del__(self):
        self.quit_driver()

    @staticmethod
    def get_yaml(filename, json_path):
        log.info('读取yaml文件：{} - {}'.format((os.path.split(filename)[-1]), json_path))
        try:
            yaml_result = YamlHandle.read_data(filename)
            return yaml_result
        except Exception as e:
            log.info('读取yaml文件 --> 失败：{}'.format(e))

    def open_url(self, url):
        """打开网址"""
        try:
            log.info('打开 {} 网址进行测试'.format(url))
            self.driver.get(url)
        except Exception as e:
            log.error('打开网址 --> 失败：{}'.format(url, e))
            assert False

    def get_current_url(self):
        url_result = self.driver.current_url
        log.info('获取当前页面的网址：{}'.format(url_result))
        return url_result

    def get_page_title(self):
        title_name = self.driver.title
        log.info('获取当前页面的名称：{}'.format(title_name))
        return title_name

    def __wait_presence(self, locator, timeout: int or float):
        """等待元素存在"""
        count_time = None
        try:
            log.info("定位元素: {}".format(locator))
            start = datetime.datetime.now()
            result = WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located(locator))
            end = datetime.datetime.now()
            count_time = (end - start).seconds
            log.info('\n耗时：{}s/{}s'.format(count_time, timeout))
            len_result = len(result)
            log.info('\n成功 -> 共 %s 个元素。' % len_result)
            if len_result == 1:
                return result[0]
            elif len_result > 1:
                return result
        except Exception as e:
            log.info('\n耗时：{}s/{}s'.format(count_time, timeout))
            log.error('\n失败：%s' % e)
            assert False

    @staticmethod
    def sleep(time01: int or float):
        log.info('强制等待：%d秒' % time01)
        time.sleep(time01)

    def shot(self, save_to_filepath):
        """
        截图
        :param save_to_filepath: 截图保存路径
        """
        try:
            log.info('截图：{}'.format(save_to_filepath))
            self.driver.save_screenshot(save_to_filepath)
        except Exception as e:
            log.error('截图：{} --> 失败：{}'.format(save_to_filepath, e))
            assert False

    def find_ele(self, locator, error_shot=0):
        """
        元素定位
        :param locator: 定位内容
        :param error_shot: 是否需要定位失败的截图（0: 不需要, 1: 需要）
        :return:
        """
        if isinstance(locator, tuple) and len(locator) == 2:
            by, element = locator
            by = by.lower()
            if 'id' in by:
                by = By.ID
            elif 'xpath' in by:
                by = By.XPATH
            elif 'class' in by:
                by = By.CLASS_NAME
            elif 'css' in by:
                by = By.CSS_SELECTOR
            elif 'tag' in by:
                by = By.TAG_NAME
            elif 'partial' not in by and 'link' in by:
                by = By.LINK_TEXT
            elif 'partial' in by and 'link' in by:
                by = By.PARTIAL_LINK_TEXT
            elif by in ['android_uiautomator', '-android uiautomator']:
                by = MobileBy.ANDROID_UIAUTOMATOR
            elif by in ['accessibility_id', 'accessibility id']:
                by = MobileBy.ACCESSIBILITY_ID
            else:
                raise NameError("你输入的元素定位方式 {} 有误".format(by))
            locator = (by, element)
            ele = self.__wait_presence(locator, 15)

            if ele:
                return ele
            elif error_shot == 1:
                mark = '异常截图'
                now_time = time.strftime('%Y%m%d%H%M%S')
                suffix = '.png'
                filepath = os.path.join(TEST_SCREENSHOT, mark + now_time + suffix)
                self.shot(filepath)
            assert False
        else:
            log.error('locator格式错误。正确案例：(定位方式, 元素内容)')
            assert False

    def click_ele(self, locator, click_model=0):
        """点击元素"""
        # doc_height = int(self.driver.execute_script('return document.body.scrollHeight;'))
        # window_height = int(self.driver.execute_script('return window.screen.height;'))
        for i in range(10):
            try:
                if 'span' in str(locator):
                    time.sleep(0.5)
                ele = self.find_ele(locator)
                log.info('点击元素')
                if isinstance(ele, list):
                    for i2 in range(len(ele)):
                        # 滚动屏幕至元素可见
                        # 注：不支持火狐浏览器。
                        self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();', ele[i2])

                        if 'svg' in str(locator) or click_model:
                            self.chains.click(ele[i2]).perform()
                            return ele
                        else:
                            ele[i2].click()
                            return ele
                else:
                    # 滚动屏幕至元素可见
                    # 注：不支持火狐浏览器。
                    self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();', ele)

                    if 'svg' in str(locator) or click_model:
                        time.sleep(0.5)
                        self.chains.click(ele).perform()
                        return ele
                    else:
                        ele.click()
                        return ele
            except WebDriverException:
                time.sleep(0.5)
                continue

    def clear_content(self, locator):
        """清空文本框"""
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        ele = self.click_ele(locator)
        try:
            action = ActionChains(self.driver)
            log.info("清空文本框")
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
            time.sleep(0.5)
            return ele
        except Exception as e:
            log.error("清空文本框 --> 失败：{}".format(e))
            assert False

    def input_content(self, locator, content, clear=0):
        """输入内容"""
        if clear:
            self.clear_content(locator)
        ele = self.find_ele(locator)
        try:
            log.info('输入内容："{}"'.format(content))
            ele.send_keys(content)
        except Exception as e:
            log.error('输入内容 --> 失败：{}'.format(e))
            assert False

    def paste_content(self, content):
        """点击文本框 并 粘贴内容"""
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        # 这个action要独立在这里，不要定义成  类属性，不然会出错的。
        # pyperclip.copy(content)
        # self.click_ele(locator)
        try:
            action = ActionChains(self.driver)
            log.info('粘贴内容："{}"'.format(content))
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).send_keys(Keys.ESCAPE).perform()
            # action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        except Exception as e:
            log.error('粘贴内容 --> 失败：{}'.format(e))
            assert False

    def get_attr(self, locator, attribute, is_del_symbol=0):
        """
        获取元素的属性
        :param locator: 元素对象
        :param attribute: 属性名字（text/id/class/tag等等）
        :param is_del_symbol: 是否需要删除各种符号
        :return:
        """
        ele = self.find_ele(locator)
        if isinstance(ele, list):
            len_ele = len(ele)
        else:
            len_ele = 1
        if attribute.lower() == "text":
            attribute = 'textContent'
        result = None
        try:
            if len_ele == 1:
                if is_del_symbol == 1:
                    log.info('获取单个元素的{}，且删除符号。'.format(attribute))
                    result = my_del_symbol(ele.get_attribute(attribute))
                else:
                    log.info('获取单个元素的{}。'.format(attribute))
                    result = ele.get_attribute(attribute)
            elif len_ele > 1 and is_del_symbol == 1:
                result = []
                log.info('获取所有元素的{}，且删除符号。'.format(attribute))
                for i in ele:
                    attr_value = my_del_symbol(i.get_attribute(attribute))
                    result.append(attr_value)
            elif len_ele > 1:
                result = []
                log.info('获取所有元素的{}。'.format(attribute))
                for i in ele:
                    attr_value = i.get_attribute(attribute)
                    result.append(attr_value)
            log.info('\n获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取失败：{}'.format(e))
            assert False

    # @staticmethod
    # def upload_file(browser, filepath):
    #     """非input标签文件上传"""
    #     try:
    #         log.info('上传文件：{}'.format(filepath))
    #         # 窗口title
    #         browser_type = {
    #             "firefox": "文件上传",
    #             "chrome": "打开",
    #             "ie": "选择要加载的文件"
    #         }
    #         # 提升容错性
    #         if browser.lower() not in browser_type.keys():
    #             browser1 = "chrome"
    #         else:
    #             browser1 = browser
    #         # 正式的操作
    #         time.sleep(2)
    #         dialog = win32gui.FindWindow("#32770", browser_type[browser1])  # 一级窗口
    #         combobox_ex32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级窗口
    #         combobox = win32gui.FindWindowEx(combobox_ex32, 0, 'ComboBox', None)  # 三级窗口
    #         edit = win32gui.FindWindowEx(combobox, 0, 'Edit', None)  # 四级窗口  -->  路径输入框
    #         button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 四级窗口  -->  打开按钮
    #         win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)  # 输入文件路径
    #         win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
    #         time.sleep(1)
    #     except Exception as e:
    #         raise Exception('上传文件 --> 失败：{}'.format(filepath, e))

    def scroll_to_ele(self, locator):
        ele = self.find_ele(locator)
        try:
            log.info('滑动屏幕 - 使元素居于屏幕底部。')
            self.driver.execute_script('arguments[0].scrollIntoView(false);', ele)
            return ele
        except Exception as e:
            log.error('滑动屏幕 - 使元素居于屏幕底部 --> 失败：{}'.format(e))
            assert False

    def swipe_screen(self, x_pixel, y_pixel):
        """自定义滑动屏幕"""
        touch = TouchActions(self.driver)
        try:
            log.info('滑动屏幕：({}，{})'.format(x_pixel, y_pixel))
            touch.scroll(x_pixel, y_pixel)
        except Exception as e:
            log.error('滑动屏幕 --> 失败：{}'.format(e))
            assert False

    def into_dialog(self):
        """进入iframe"""
        log.info('进入会话框。')
        try:
            alert = WebDriverWait(self.driver, 15).until(ec.alert_is_present())
            return alert
        except Exception as e:
            log.error('进入会话框 --> 失败：{}'.format(e))

    def confirm_dialog(self):
        """会话（alert、confirm窗口）,点击确认"""
        alert = self.into_dialog()
        try:
            log.info('处理会话框 --> 确认。')
            alert.accept()
        except Exception as e:
            log.error('处理会话框 --> 确认失败：{}'.format(e))
            assert False

    def cancel_dialog(self):
        """会话（alert、confirm窗口）,点击取消"""
        alert = self.into_dialog()
        try:
            log.info('处理会话框 --> 取消。')
            alert.dismiss()
        except Exception as e:
            log.error('处理会话框 --> 取消失败：{}'.format(e))
            assert False

    def send_keys_dialog(self, content):
        """
        会话（prompt窗口）,点击输入内容
        :param content: 输入的内容
        """
        alert = self.into_dialog()
        try:
            log.info('处理会话框 --> 输入内容：{}'.format(content))
            alert.send_keys(content)
        except Exception as e:
            log.error('处理会话框 --> 输入内容失败：{}'.format(e))
            assert False

    def get_text_dialog(self):
        """会话（alert、confirm、prompt窗口）,点击获取文本"""
        alert = self.into_dialog()
        try:
            log.info('处理会话框 --> 获取文本。')
            alert_text = alert.text
            return alert_text
        except Exception as e:
            log.error('处理会话框 --> 获取文本失败：{}'.format(e))
            assert False

    def into_frame(self, locator):
        """进入iframe"""
        ele = self.find_ele(locator)
        log.info('进入iframe：{}'.format(locator))
        self.driver.switch_to.frame(ele)

    def quit_one_frame(self):
        """退出一个iframe"""
        log.info('处理frame --> 退出到上一级'.format())
        self.driver.switch_to.parent_frame()

    def quit_all_frame(self):
        """退出iframe，到主HTML"""
        log.info('处理frame --> 退出到主HTML'.format())
        self.driver.switch_to.default_content()

    def current_window(self):
        """当前在第几个浏览器窗口"""
        window_handle_list = self.driver.window_handles
        current_window = window_handle_list.index[self.driver.current_window()] + 1
        log.info('浏览器窗口 --> 第{}/共{}}'.format(current_window, len(window_handle_list)))
        return current_window

    def open_new_window(self, url=None):
        """
        打开新的浏览器窗口
        :param url: 要打开的网址
        """
        js = "window.open('%s')" % url
        log.info('浏览器窗口 --> 新开 {}'.format(url))
        self.driver.execute_script(js)

    def switch_window(self, window_order: int):
        """
        进入某一个浏览器窗口
        :param window_order: 窗口下标
        """
        window_handle_list = self.driver.window_handles
        log.info('浏览器窗口 --> 第{}/共{}'.format(window_order, len(window_handle_list)))
        self.driver.switch_to.window(window_handle_list[window_order - 1])

    def quit_driver(self):
        log.info('driver --> 退出')
        self.driver.quit()

    def back_driver(self, sleep_time: int or float):
        time.sleep(sleep_time)
        log.info('等待 {}s --> driver --> 返回'.format(sleep_time))
        self.driver.back()

    def refresh_driver(self, sleep_time: int or float):
        log.info('等待 {}s --> driver --> 刷新'.format(sleep_time))
        time.sleep(sleep_time)
        self.driver.refresh()


class APPBasePage(UIBasePages):

    def click_pixels(self, coordinate: list):
        """
        多点点击坐标点
        example:
            pixels = [(448, 437), (448, 720), (440, 992), (720, 992)]  # list内嵌tuple
            click_pixels(pixels)
        """
        try:
            log.info('多点点击：{}'.format(coordinate))
            self.driver.tap(coordinate)
        except Exception as e:
            log.error('多点点击 --> 失败：{}'.format(e))

    def get_toast_text(self, locator):
        """
        获取toast元素的属性
        :param locator: 元素对象
        :return: 返回一个str
        """
        by, element = locator
        if by.lower() != 'xpath':
            log.error('元素查找方式有误，必须用xpath定位 ！！！')
            assert False
        ele = self.find_ele(locator)
        try:
            log.info('获取 toast提示框 的 text。')
            result = ele.text
            log.info('\n获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取 toast提示框 的 text --> 失败：{}'.format(e))
            assert False

    def get_ele_location(self, locator):
        """获取元素坐标"""
        log.info('获取元素坐标：{}'.format(locator))
        element_location = self.find_ele(locator).location
        log.info('\n获取到的坐标：{}'.format(element_location))
        return element_location

    def get_screen_size(self):
        """获取屏幕尺寸"""
        log.info('获取屏幕尺寸:')
        screen_size = self.driver.get_window_size()
        log.info('\n屏幕的尺寸：{}'.format(screen_size))
        return screen_size

    def swipe_for(self, direction: str, duration=500):
        """
        屏幕滑动
        :param direction: 方位
        :param duration: 滑动速度（默认0.5S/次）
        :return:
        """
        direction = direction.lower()
        directions = ['up', 'down', 'left', 'right']
        if direction not in directions:
            log.error(f'屏幕滑动 --> 失败: {"方位输入错误，只能输入 up、down、left、right"}')
        screen_size = self.get_screen_size()
        x_relative = 0.5
        y_relative = 0.5
        init_x = screen_size['width']
        init_y = screen_size['height']

        if direction == 'up':
            start_x = init_x * x_relative
            start_y = init_y * 0.7
            end_x = start_x
            end_y = init_y * 0.2
            direction_name = '上'
        elif direction == 'down':
            start_x = init_x * x_relative
            start_y = init_y * 0.2
            end_x = start_x
            end_y = init_y * 0.7
            direction_name = '下'
        elif direction == 'left':
            start_x = init_x * 0.2
            start_y = init_y * y_relative
            end_x = init_x * 0.9
            end_y = start_y
            direction_name = '左'
        else:
            start_x = init_x * 0.9
            start_y = init_y * y_relative
            end_x = init_x * 0.2
            end_y = start_y
            direction_name = '右'

        try:
            log.error(f'屏幕滑动({direction_name}): ({start_x}, {start_y}) -> ({end_x}, {end_y})')
            self.driver.swipe(start_x, start_y, end_x, end_y, duration=duration)
        except Exception as e:
            log.error(f'屏幕滑动({direction_name}) --> 失败：{e}')
            assert False

    def get_all_context(self):
        """获取所有上下文"""
        log.info('获取所有上下文')
        context_list = self.driver.contexts
        log.info('\n所有上下文：{}'.format(context_list))
        return context_list

    def get_current_context(self):
        """获取现在所在的上下文"""
        log.info('获取现在所在的上下文')
        current_context = self.driver.current_context
        log.info('\n现在所在的上下文是：{}'.format(current_context))
        return current_context

    def switch_context(self, context):
        """切换上下文"""
        try:
            log.info('进入上下文：{}'.format(context))
            self.driver.switch_to.context(context)
        except Exception as e:
            log.error('进入上下文 --> 失败：{}'.format(e))
            assert False

    def switch_native_app(self):
        """切换回原生页面"""
        try:
            log.info('返回原生上下文。')
            self.driver.switch_to.context('NATIVE_APP')
        except Exception as e:
            log.error('返回原生上下文 --> 失败：{}'.format(e))
            assert False

    def ligature_pixels(self, pixel_list: list):
        """
        解锁
        example:
            pixels = [(448, 437), (448, 720), (440, 992), (720, 992)]  # list内嵌tuple
            ligature_pixels(pixels)
        """
        touch = TouchAction(self.driver)
        log.info('解锁开始：{}'.format(pixel_list[0]))
        touch.long_press(x=pixel_list[0][0], y=pixel_list[0][1])
        time.sleep(1)  # 代码的执行为毫秒级，APP的反应没那么快，所以这里要等待，不然多半是按不上的
        for i in range(1, len(pixel_list)):
            log.info('\n连接：({}, {})'.format(pixel_list[i][0], pixel_list[i][1]))
            touch.move_to(x=pixel_list[i][0], y=pixel_list[i][1]).wait(1)
        touch.release().perform()
