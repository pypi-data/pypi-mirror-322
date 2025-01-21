"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-01-21
Author: Martian Bugs
Description: 团队管理数据采集
"""

from DrissionPage import Chromium

from .anchor import Anchor


class TeamManage:
    def __init__(self, browser: Chromium):
        self._browser = browser

        self._anchor = None

    @property
    def anchor(self):
        """主播排行"""

        if not self._anchor:
            self._anchor = Anchor(self._browser)

        return self._anchor
