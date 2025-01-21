import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Literal

from .._types import FilteredDataclass


@dataclass
class GetterFilter:
    """记录筛选器"""

    field: str
    operator: Literal[
        'equal', 'notEqual', 'incontain', 'notContain', 'empty', 'notEmpty'
    ]
    value: list[str] = None


@dataclass
class Updater:
    """记录更新器"""

    record_id: str
    fields: dict[str, any]

    def to_dict(self):
        return self.__dict__


@dataclass
class GetterResult(metaclass=FilteredDataclass):
    """获取器结果"""

    nextCursor: str = None
    records: list[dict] = None
    hasMore: bool = False

    def __post_init__(self):
        if self.records and isinstance(self.records, list):
            self.records = self.__records_handle()

    def __records_handle(self):
        records: list[dict] = []
        for record in self.records:
            record_temp = {'id': record.get('id'), 'fields': {}}
            fields: dict = record.get('fields')

            for field_name, field_value in fields.items():
                _value = deepcopy(field_value)
                if isinstance(field_value, dict):
                    if 'link' in field_value:
                        _value = field_value.get('link')
                    elif 'name' in field_value:
                        _value = field_value.get('name')

                record_temp['fields'][field_name] = _value

            records.append(record_temp)

        return records

    def to_file(self, file_path: str):
        """
        将数据写出到本地

        Args:
            file_path: 用于存储数据的文件路径
        Returns:
            格式化后的 json 字符串
        """

        if not self.records:
            raise ValueError('数据记录为空, 无法写出')

        json_str = json.dumps(self.records, ensure_ascii=False, indent=2)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

        return json_str


@dataclass
class AdderResult(metaclass=FilteredDataclass):
    """新增器结果"""

    result: list[str] = None
    """新增的记录id列表"""
    success: bool = None
    errorMsg: str = None


@dataclass
class UpdaterResult(metaclass=FilteredDataclass):
    """更新器结果"""

    result: list[dict] = None
    """更新的记录列表"""
    success: bool = None
    errorMsg: str = None


@dataclass
class DeletorResult(metaclass=FilteredDataclass):
    """删除器结果"""

    result: list[str] = None
    """删除的记录id列表"""
    success: bool = None
    errorMsg: str = None
