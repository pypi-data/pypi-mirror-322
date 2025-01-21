"""
Copyright (c) 2024-now LeslieLiang All rights reserved.
Build Date: 2024-12-18
Author: LeslieLiang
Description: 多维表连接流SDK
"""

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from ._table.table import Table


@dataclass
class ViewUrl:
    """视图链接对象"""

    url: str = None
    did: str = None
    """文档id"""
    tid: str = None
    """数据表id"""


class ComplexTable:
    def __init__(self, flow_url: str):
        """
        初始化 ComplexTable 类
        Args:
            flow_url: 连接流 url
        """

        self.flow_url = flow_url

    def _parse_view_url(self, view_url: str):
        """
        解析视图链接

        Args:
            view_url: 视图链接
        Returns:
            ViewUrl 对象
        """

        if not view_url or not isinstance(view_url, str):
            raise ValueError('view_url 参数不能为空或非字符串类型')

        parsed_url = urlparse(view_url)
        url_path_splited = parsed_url.path.split('/')
        did = url_path_splited[-1]

        query_dict = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        iframeQuery = query_dict.get('iframeQuery')
        tid = parse_qs(iframeQuery).get('sheetId')[0]

        return ViewUrl(url=view_url, did=did, tid=tid)

    def get_table(self, did: str, tid: str) -> Table:
        """
        获取表格对象
        Args:
            did: 文档 id
            tid: 数据表 id
        Returns:
            Table 对象
        """

        return Table(self.flow_url, did, tid)

    def get_table_by_view_url(self, url: str):
        """
        通过视图链接获取表格对象
        - 解析视图链接获取其中的文档id和视图id

        Args:
            url: 视图链接
        Returns:
            Table 对象
        """

        view_url = self._parse_view_url(view_url=url)
        return self.get_table(did=view_url.did, tid=view_url.tid)
