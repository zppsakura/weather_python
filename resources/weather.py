
from flask_restful import reqparse, request, Resource

import requests
import resources.common as common
from resources.common import *
import pymongo
import json

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 和云天气api的key
KEY = '56931e6bdfa14180a5e9ab6594917742'

"""
和云天气api的url
%s 为 查询类型:
now 实况天气、
forecast 3-10天预报、
hourly 逐小时预报、
lifestyle 生活指数
"""
URL = 'https://free-api.heweather.net/s6/weather/%s'

TYPE_NOW = 'now'
TYPE_FORECAST = 'forecast'

# 和云天气结果json的key
HE_WEATHER_KEY = 'HeWeather6'

ARGS_LOCATION = 'location'

BASIC_LOCATION = 'basic.location'

IS_UPDATE = 'isUpdate'

# 解析location参数
parser = reqparse.RequestParser()
parser.add_argument(ARGS_LOCATION)


class Weather(Resource):
    STATUS = 'status'
    OK = 'ok'

    def __init__(self):
        # 连接MongoDB
        self.client = pymongo.MongoClient('localhost')
        # 指定数据库
        self.dblist = self.client.weather
        # 指定集合
        self.collection = self.dblist.weathers

    # 保存天气数据到mongo
    def saveWeather(self, location, data):
        if self.collection.find_one({BASIC_LOCATION: location}):
            self.collection.update({BASIC_LOCATION: location}, data)
            return '更新成功'
        else:
            self.collection.insert_one(data)
            # 插入mongo之后data会被填充_id导致flask返回时产生异常,这里需要清除一下_id
            del data[MONGO_ID]
            return '添加成功'

    def deleteWeather(self, location):
        ret = self.collection.remove({BASIC_LOCATION: location})
        if ret['n'] > 0:
            return '删除成功'
        else:
            return '删除失败'

    # 通过地址查询天气
    def getNowWeatherByLocation(self, location):
        payload = {ARGS_LOCATION: location, 'key': KEY}
        # 将查询类型注入到url
        res = requests.get(URL % TYPE_NOW, payload)
        weather = res.json()[HE_WEATHER_KEY]
        if len(weather) > 0:
            ret = weather[0]
            logger.info(ret)
            return ret

    # 查询天气的方法
    def getForecastWeatherByLocation(self, location):
        payload = {ARGS_LOCATION: location, 'key': KEY}
        # 将查询类型注入到url
        res = requests.get(URL % TYPE_FORECAST, payload)

        weather = res.json()[HE_WEATHER_KEY]
        if len(weather) > 0:
            ret = weather[0]
            return ret

    def post(self):
        # 解析json中的地址
        location = request.get_json()[ARGS_LOCATION]
        # 获取和云天气api中的天气数据
        weather = self.getNowWeatherByLocation(location)
        if not weather:
            return common.error()
        # 判断查询状态
        status = weather[self.STATUS]
        if status == self.OK:
            msg = self.saveWeather(location, weather)
            return common.success(weather, msg)
        else:
            return common.error(status)

    def get(self):
        # 解析params
        args = parser.parse_args()
        location = args[ARGS_LOCATION]
        # 获取和云天气api中的天气数据
        weather = self.getForecastWeatherByLocation(location)
        if not weather:
            return common.error()
        # 判断查询状态
        status = weather[self.STATUS]
        if status == self.OK:
            self.saveWeather(location, weather)
            return common.success(weather)
        else:
            return common.error(status)

    def delete(self):
        # 解析json中的地址
        location = request.get_json()[ARGS_LOCATION]
        msg = self.deleteWeather(location)
        return common.success(None, msg)
