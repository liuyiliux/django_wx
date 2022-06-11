#-*- codeing = utf-8 -*-
#@Time: 2022/5/21 21:54
#@Author: 怪盗LLYL
#@File: weatherInfo_utils.py
#@Software: PyCharm
import json
import requests
from django_wx import  settings
class Gaode_tianqi(object):
    def __init__(self,address):
        self.__address = address
        self.key = settings.GAODE_KEY
        url = f"https://restapi.amap.com/v3/geocode/geo?address={self.__address}&output=JSON&key={self.key}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        adcode = json.loads(response.text)["geocodes"][0]["adcode"]
        self.__adcode = adcode
        basejson = self.get_weatherinfo_base()
        self.__city = basejson["lives"][0]["city"] #城市名称
        self.__weather = basejson["lives"][0]["weather"] #天气现象（汉字描述）
        self.__temperature = basejson["lives"][0]["temperature"] #实时气温，单位：摄氏度
        self.__winddirection = basejson["lives"][0]["winddirection"] #风向描述
        self.__windpower = basejson["lives"][0]["windpower"] #风力级别，单位：级
        self.__humidity = basejson["lives"][0]["humidity"] #空气湿度
        self.__reporttime = basejson["lives"][0]["reporttime"] #数据发布的时间
        self.__forecastlist = self.get_weatherinfo_all()["forecasts"][0]["casts"]

    def __str__(self):
        str = "未来天气：\r\n"
        for i in self.__forecastlist:
            str = str+f" 日期：{i['date']} 星期{i['week']} 白:{i['dayweather']} {i['daytemp']}℃  风向：{i['daywind']}  风力：{i['daypower']} 夜:{i['nightweather']} {i['nighttemp']}℃ 风向：{i['nightwind']}  风力：{i['nightpower']}\r\n"
        return f"城市：{self.__city} 当前温度：{self.__temperature}℃ 天气：{self.__weather} 风向：{self.__winddirection} 湿度：{self.__humidity} 发布时间：{self.__reporttime}\n{str}"
    @property
    def forecastlist(self):
        return (self.__forecastlist)
    @property
    def reporttime(self):
        return (self.__reporttime)
    @property
    def windpower(self):
        return (self.__windpower)
    @property
    def humidity(self):
        return (self.__humidity)
    @property
    def city(self):
        return (self.__city)
    @property
    def winddirection(self):
        return (self.__winddirection)
    @property
    def temperature(self):
        return (self.__temperature)
    @property
    def weather(self):
        return (self.__weather)
    @property
    def address(self):
        return (self.__address)

    @property
    def adcode(self):
        return self.__adcode

    def get_weatherinfo_base(self):
        import requests
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={self.__adcode}&extensions=base&output=JSON"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return  json.loads(response.text)
    def get_weatherinfo_all(self):
        import requests
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={self.__adcode}&extensions=all&output=JSON"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return  json.loads(response.text)

if __name__ == '__main__':
    listcity = ["北京","营口","上海","无锡","宁波","扬州"]
    for i in listcity:
        tianqi = Gaode_tianqi(i)
        print(tianqi)