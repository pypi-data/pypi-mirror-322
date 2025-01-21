"""
商家后台-多多客服数据采集器
"""

from DrissionPage import Chromium

from .._utils import Utils
from ._dict import Dictionary
from ._utils import pick__custom_date_range


class Urls:
    service = 'https://mms.pinduoduo.com/mms-chat/overview/service'
    sales = 'https://mms.pinduoduo.com/mms-chat/overview/marketing'


class DataPacketUrls:
    service__overview = 'mms.pinduoduo.com/desert/stat/mallServiceOverviewData'
    sales__overview = 'mms.pinduoduo.com/desert/stat/mallSalesOverviewData'


class CustomerService:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def get__service__overview(self, date: str, timeout: float = None, raw=False):
        """
        [多多客服-客服数据-服务数据概览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()

        page.listen.start(
            targets=DataPacketUrls.service__overview, method='POST', res_type='Fetch'
        )
        page.get(Urls.service)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.service__overview, method='POST', res_type='Fetch'
        )
        if date == Utils.date_yesterday():
            yesterday_btn_ele = page.ele('t:button@@text()=近1天', timeout=3)
            if not yesterday_btn_ele:
                raise ValueError('未找到 [近1天] 按钮')

            yesterday_btn_ele.click()
        else:
            pick__custom_date_range(begin_date=date, end_date=date, page=page)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('获取数据包超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.customer_service.service__overview
        )
        record = Utils.dict_format__round(
            record, fields=['平均人工响应时长'], precision=0
        )
        record = Utils.dict_format__ratio(record, fields=['3分钟人工回复率'])

        return record

    def get__sales__overview(self, date: str, timeout: float = None, raw=False):
        """
        [多多客服-客服数据-销售数据概览] 数据获取
        - 只能获取前3天的数据, 例如 18 号只能获取 15 号的数据
        - 如果获取的日期大于3天前, 将返回空数据
        """

        min_date = Utils.date_calculate(days=3)
        if Utils.date_diff_days(date, min_date) > 0:
            return

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.sales__overview, method='POST', res_type='Fetch'
        )
        page.get(Urls.sales)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.sales__overview, method='POST', res_type='Fetch'
        )
        if date == min_date:
            # 如果指定的日期刚好等于 3 天前的日期, 则可以直接点击近 1 天按钮
            quick_btn_ele = page.ele('t:button@@text()=近1天', timeout=3)
            if not quick_btn_ele:
                raise ValueError('未找到 [近1天] 按钮')

            quick_btn_ele.click(by_js=True)
        else:
            pick__custom_date_range(begin_date=date, end_date=date, page=page)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('获取数据包超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(result, Dictionary.customer_service.sales__overview)
        record = Utils.dict_format__ratio(record, fields=['询单转化率'])
        record = Utils.dict_format__round(record, fields=['询单转化率'])

        return record
