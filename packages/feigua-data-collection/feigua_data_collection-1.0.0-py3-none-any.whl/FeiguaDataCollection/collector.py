"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-01-21
Author: Martian Bugs
Description: 数据采集器
"""

from DrissionPage import Chromium, ChromiumOptions

from .team_manage.team_manage import TeamManage


class Collector:
    """采集器. 使用之前请先调用 `connect_browser` 方法连接浏览器."""

    def __init__(self):
        self.browser = None

        self._team_manage = None

    def connect_browser(self, port: int):
        """
        连接浏览器

        Args:
            port: 浏览器调试端口号
        """

        chrome_options = ChromiumOptions(read_file=False)
        chrome_options.set_local_port(port=port)

        self.browser = Chromium(addr_or_opts=chrome_options)

    @property
    def team_manage(self):
        """团队管理"""

        if self._team_manage is None:
            self._team_manage = TeamManage(self.browser)

        return self._team_manage
