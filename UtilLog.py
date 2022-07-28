#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 15:32
# @Author  : Issac
# @Email   : Issac_czy@163.com
# @File    : UtilLog.py
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/info_{0}.log".format(datetime.now().strftime('%Y%m%d')))
handler.setLevel(logging.INFO)  # 输出到文件的日志等级
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)  # 输出日志的格式模板
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)


class MyLogger:

    @staticmethod
    def info(msg):
        """
        打印日志消息
        :param msg:
        :return:
        """
        logger.info(msg)

    @staticmethod
    def error(msg):
        """
        打印日志消息
        :param msg:
        :return:
        """
        logger.error(msg)
