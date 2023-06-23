#-*- codeing = utf-8 -*-
#@Time: 2023/6/19 23:16
#@Author: 怪盗LLYL
#@File: qqutils.py
#@Software: PyCharm
import requests


def jscode2session(code):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:{'status': True, 'data': {...}}
    """
    headers = {
    }
    params = (
        ('appid', 'wxb35a6c056ae02697'),
        ('secret', '284cd3afeeb59cacfc0356a9c4b61a50'),
        ('js_code', code),
        ('grant_type', 'authorization_code'),
    )
    response = requests.get('https://api.weixin.qq.com/sns/jscode2session', headers=headers, params=params)
    rspdata = response.json()
    result = {}
    if rspdata.get('errcode') == 0:
        result['status'] = True
        result['data'] = rspdata
    elif len(rspdata.get('session_key'))>0 and len(rspdata.get('openid') )>0:
        result['status'] = True
        result['data'] = rspdata
    elif rspdata.get('errcode')== 40029:
        result['status'] = False
        result['error'] = 'code 无效'
    elif rspdata.get('errcode') == 45011:
        result['status'] = False
        result['error'] = '频率限制，每个用户每分钟100次'
    elif rspdata.get('errcode') == -1:
        result['status'] = False
        result['error'] = '系统繁忙，此时请开发者稍候再试'
    else:
        result['status'] = False
        result['error'] = '其他错误'
    return result