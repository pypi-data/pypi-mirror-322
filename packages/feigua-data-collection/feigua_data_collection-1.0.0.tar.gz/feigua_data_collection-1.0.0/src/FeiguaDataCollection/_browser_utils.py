"""
浏览器工具集
"""

from DrissionPage import Chromium


class BrowserUtils:
    @staticmethod
    def get__main_page(browser: Chromium):
        """
        获取主要页面的浏览器标签页
        - 如果没有找到，则新建一个标签页并返回
        """

        page = browser.get_tab(title='飞瓜智投')
        if not page:
            page = browser.new_tab()

        return page
