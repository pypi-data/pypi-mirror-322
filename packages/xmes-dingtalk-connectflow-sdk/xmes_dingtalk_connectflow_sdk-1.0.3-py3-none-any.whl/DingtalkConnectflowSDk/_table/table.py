from typing import Any, Literal

from requests import post

from ._types import (
    AdderResult,
    DeletorResult,
    GetterFilter,
    GetterResult,
    Updater,
    UpdaterResult,
)


class Table:
    __HEADERS = {
        'Content-Type': 'application/json',
    }

    def __init__(self, flow_url: str, did: str, tid: str):
        self.flow_url = flow_url
        self.did = did
        self.tid = tid
        self.global_reqdata = {
            'did': did,
            'tid': tid,
        }

    def __verify_records(self, records: list[Any], record_type: object):
        """
        records 参数校验
        - 校验失败, 抛出 ValueError 异常
        - 校验成功, 返回清洗后的 records 列表

        Args:
            records: 记录列表
            record_type: 记录类型
        """

        if not records or not isinstance(records, list):
            raise ValueError('records 参数需要是列表类型且不能为空')

        records_clean = [
            record for record in records if record and isinstance(record, record_type)
        ]
        if not records_clean:
            record_type_name = record_type.__qualname__
            raise ValueError(
                f'records 列表经过判断清洗后, 未在其中找到有效的 {record_type_name}'
            )

        return records_clean

    def get(
        self,
        size=20,
        cursor: str = '',
        combination: Literal['and', 'or'] = 'and',
        filters: list[GetterFilter] | None = None,
    ):
        """
        获取表格数据
        Args:
            size: 每页数据条数, 默认为 20
            cursor: 分页游标, 首次请求可不传, 后续需传入上一次返回的 nextCursor 值
            combination: 组合方式
            filters: 过滤条件
        Returns:
            GetterResult 对象
        """

        reqdata = {
            **self.global_reqdata,
            'handle': 'GET',
            'handle_get': {
                'size': size,
                'cursor': cursor,
            },
        }

        if combination and combination in ['and', 'or']:
            filter_field = {}
            filter_field['combination'] = combination
            if filters and isinstance(filters, list):
                conditions = [
                    item.__dict__ for item in filters if isinstance(item, GetterFilter)
                ]
                filter_field['conditions'] = conditions
            reqdata['handle_get']['filter'] = filter_field

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        resp_json: dict = resp.json()
        result: dict = resp_json.get('GET_RESULT')
        if not result or not isinstance(result, dict):
            raise ValueError('返回的数据中未找到 GET_RESULT 字段或该字段非字典类型')

        getter_result = GetterResult(**result)

        return getter_result

    def add(self, records: list[dict]):
        """
        新增记录
        Args:
            records: 用于新增的记录列表
        Returns:
            AdderResult 对象
        """

        records_clean = self.__verify_records(records, dict)

        reqdata = {
            **self.global_reqdata,
            'handle': 'ADD',
            'handle_add': {
                'records': records_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        resp_json: dict = resp.json()
        result: dict = resp_json.get('ADD_RESULT')
        if not result or not isinstance(result, dict):
            raise ValueError('返回的数据中未找到 ADD_RESULT 字段或该字段非字典类型')

        adder_result = AdderResult(**result)

        return adder_result

    def update(self, records: list[Updater]):
        """
        更新记录
        Args:
            records: 更新记录列表
        Returns:
            UpdaterResult 对象
        """

        records_clean: list[Updater] = self.__verify_records(records, Updater)
        records_clean = [record.to_dict() for record in records_clean]

        reqdata = {
            **self.global_reqdata,
            'handle': 'UPDATE',
            'handle_update': {
                'records': records_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        resp_json: dict = resp.json()
        result: dict = resp_json.get('UPDATE_RESULT')
        if not result or not isinstance(result, dict):
            raise ValueError('返回的数据中未找到 UPDATE_RESULT 字段或该字段非字典类型')

        updater_result = UpdaterResult(**result)

        return updater_result

    def delete(self, record_ids: list[str]):
        """
        删除记录
        Args:
            record_ids: 记录 id 列表
        Returns:
            DeletorResult 对象
        """

        record_ids_clean = self.__verify_records(record_ids, str)

        reqdata = {
            **self.global_reqdata,
            'handle': 'DELETE',
            'handle_delete': {
                'record_ids': record_ids_clean,
            },
        }

        resp = post(self.flow_url, json=reqdata, headers=self.__HEADERS)
        resp_json: dict = resp.json()
        result: dict = resp_json.get('DELETE_RESULT')
        if not result or not isinstance(result, dict):
            raise ValueError('返回的数据中未找到 DELETE_RESULT 字段或该字段非字典类型')

        deletor_result = DeletorResult(**result)

        return deletor_result
