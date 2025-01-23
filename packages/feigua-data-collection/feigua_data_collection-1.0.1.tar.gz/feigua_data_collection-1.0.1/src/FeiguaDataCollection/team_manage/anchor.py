"""
团队管理-主播排行数据采集
"""

from DrissionPage import Chromium
from DrissionPage._pages.mix_tab import MixTab

from .._browser_utils import BrowserUtils
from .._utils import Utils
from ._dict import Dictionary
from ._utils import pick__custom_date_range


class Urls:
    anchor_rank = 'https://zhitou.feigua.cn/console/child/anchor'


class DataPacketUrls:
    anchor_rank = 'zhitou.feigua.cn/api/biz/v2/Anchor/Anchor/rank_data'


class Anchor:
    """主播排行, 如果已经打开了飞瓜智投页面将托管, 否则会打开新的标签页"""

    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def _enter_check(self, page: MixTab, timeout: float = None):
        """页面进入检测, 如果失败将抛出异常"""

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page.listen.start(
            targets=DataPacketUrls.anchor_rank,
            method='GET',
            res_type='XHR',
        )
        if not Utils.same_url(Urls.anchor_rank, page.url):
            page.get(Urls.anchor_rank)
        else:
            page.refresh()

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('页面打开后数据包获取超时, 可能访问异常')

    def get__anchor_rank__detail(self, begin_date: str, end_date: str):
        """获取主播排行-表格数据"""

        page = BrowserUtils.get__main_page(self._browser)
        self._enter_check(page)

        page.listen.start(
            targets=DataPacketUrls.anchor_rank, method='GET', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        packet = page.listen.wait(timeout=15)
        if not packet:
            raise TimeoutError('修改日期后数据包获取超时')

        resp: dict = packet.response.body
        data_list: list[dict] = resp.get('data')
        if isinstance(data_list, list) and len(data_list) == 0:
            raise ValueError('数据中的 data 字段为空列表, 可能没有数据')

        records = []
        for data in data_list:
            manager = data.get('manager').get('name')

            record = Utils.dict_mapping(data, Dictionary.anchor.anchor_rank__detail)
            record['主播'] = manager

            record = Utils.dict_format__float(
                record,
                fields=[
                    '销售额',
                    '小时成交额',
                    'UV价值',
                    '千川消耗(全域)',
                    '有效金额(含优惠券)',
                    '客单价',
                    'GPM',
                    '退款金额(店铺)',
                    '成交订单金额(含优惠券)',
                    '有效金额(店铺)',
                    '成交订单金额(店铺)',
                    '退款金额(含优惠券)',
                    '总投放消耗',
                    '优惠券金额(全域)',
                    '总成交优惠券金额',
                ],
            )
            record['直播时长'] = Utils.seconds_to_time(record['直播时长(秒)'])
            record['平均停留时长'] = Utils.seconds_to_time(record['平均停留时长(秒)'])

            records.append(record)

        return records

    def get__field_control_rank__detail(self, begin_date: str, end_date: str):
        """获取场控排行-表格数据"""

        page = BrowserUtils.get__main_page(self._browser)
        self._enter_check(page)

        # ========== 切换到场控标签页 ==========
        page.listen.start(
            targets=DataPacketUrls.anchor_rank, method='GET', res_type='XHR'
        )
        target_tab_ele = page.ele(
            'c:div[data-action_name="Team_Rank_FieldControl"]', timeout=3
        )
        if not target_tab_ele:
            raise RuntimeError('未找到 [场控] 标签页')

        page.listen.start(
            targets=DataPacketUrls.anchor_rank, method='GET', res_type='XHR'
        )
        target_tab_ele.click(by_js=True)
        if not page.listen.wait(timeout=15):
            raise RuntimeError('场控数据获取失败, 可能页面访问失败')
        # ========== 切换到场控标签页 ==========

        page.listen.start(
            targets=DataPacketUrls.anchor_rank, method='GET', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        packet = page.listen.wait(timeout=15)
        if not packet:
            raise TimeoutError('修改日期后数据包获取超时')

        resp: dict = packet.response.body
        data_list: list[dict] = resp.get('data')
        if isinstance(data_list, list) and len(data_list) == 0:
            raise ValueError('数据中的 data 字段为空列表, 可能没有数据')

        records = []
        for data in data_list:
            manager = data.get('manager').get('name')

            record = Utils.dict_mapping(data, Dictionary.anchor.anchor_rank__detail)
            record['场控'] = manager

            record = Utils.dict_format__float(
                record,
                fields=[
                    '销售额',
                    '小时成交额',
                    'UV价值',
                    '千川消耗(全域)',
                    '有效金额(含优惠券)',
                    '客单价',
                    'GPM',
                    '退款金额(店铺)',
                    '成交订单金额(含优惠券)',
                    '有效金额(店铺)',
                    '成交订单金额(店铺)',
                    '退款金额(含优惠券)',
                    '总投放消耗',
                    '优惠券金额(全域)',
                    '总成交优惠券金额',
                ],
            )
            record['直播时长'] = Utils.seconds_to_time(record['直播时长(秒)'])
            record['平均停留时长'] = Utils.seconds_to_time(record['平均停留时长(秒)'])

            records.append(record)

        return records
