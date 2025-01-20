# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-06 09:39:45
@LastEditTime: 2025-01-20 14:35:07
@LastEditors: HuangJianYi
@Description: 
"""

# 此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class CdpWorkInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(CdpWorkInfoModel, self).__init__(CdpWorkInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    # 方法扩展请继承此类

class CdpWorkInfo:

    def __init__(self):
        super(CdpWorkInfo, self).__init__()
        self.id = 0  # id
        self.business_id = 0  # 商家标识
        self.store_id = 0  # 店铺标识
        self.work_name = ""  # 作业名称(对应函数名)
        self.work_desc = ""  # 作业描述
        self.is_open = 0  # 是否开启(1-是 0-否)
        self.progress_type = 0  # 进度类型(0-未开始 1-进行中 2-已完成)
        self.step_value = 0  # 步骤值
        self.run_desc = ""  # 运行结果描述
        self.run_start_date = '1970-01-01 00:00:00.000'  # 开始运行时间
        self.run_end_date = '1970-01-01 00:00:00.000'  # 结束运行时间
        self.run_last_date = '1970-01-01 00:00:00.000'  # 最近运行时间
        self.create_date = '1970-01-01 00:00:00.000'  # 创建时间

    @classmethod
    def get_field_list(self):
        return [
            'id', 'business_id', 'store_id', 'work_name', 'work_desc',
            'is_open', 'progress_type', 'step_value', 'run_desc',
            'run_start_date', 'run_end_date', 'run_last_date', 'create_date'
        ]

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "cdp_work_info_tb"
