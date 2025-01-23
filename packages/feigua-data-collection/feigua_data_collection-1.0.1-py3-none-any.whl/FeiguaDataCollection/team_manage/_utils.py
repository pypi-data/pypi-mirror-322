from time import sleep

from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.common import Keys


def pick__custom_date_range(begin_date: str, end_date: str, page: MixTab):
    """
    修改自定义日期范围

    Args:
        begin_date: 开始日期
        end_date: 结束日期
        page: 网页对象
    """

    mapping = [['开始日期', begin_date], ['结束日期', end_date]]
    for item in mapping:
        date_input_ele = page.ele(f'c:input[placeholder="{item[0]}"]', timeout=3)
        if not date_input_ele:
            raise RuntimeError(f'未找到 [{item[0]}] 输入框')

        date_input_ele.input(item[1] + Keys.ENTER, clear=True)
        sleep(0.5)
