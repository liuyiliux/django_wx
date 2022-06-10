#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jwt
import datetime
from jwt import exceptions
from django_wx import  settings

JWT_SALT = settings.SECRET_KEY


def create_token(payload, timeout=24):
    """
    :param payload:  例如：{'username':'lyl'}用户信息
    :param timeout: token的过期时间，默认20分钟
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=timeout)
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, algorithms=["HS256"])  # payload为中间的第二段
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result
if __name__ == '__main__':
    payload = {'a':'b'}
    a = create_token(payload)
    print(a)
    print(parse_payload(a))
