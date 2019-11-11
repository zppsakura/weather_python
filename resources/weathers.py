from flask_restful import request, Resource
import resources.common as common
from resources.common import *
import pymongo
import json

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Weathers(Resource):
    def __init__(self):
        # 连接MongoDB
        self.client = pymongo.MongoClient('localhost')
        # 指定数据库
        self.dblist = self.client.weather
        # 指定集合
        self.collection = self.dblist.weathers

    def selectWeathers(self):
        weathers = self.collection.find()
        weathersRet = []
        for weather in weathers:
            # 插入mongo之后data会被填充_id导致flask返回时产生异常,这里需要清除一下_id
            del weather[MONGO_ID]
            weathersRet.append(weather)
        return weathersRet

    # 查询天气的方法
    def get(self):
        weathers = self.selectWeathers()
        if weathers:
            return common.success(data=weathers)
        else:
            return common.error()
