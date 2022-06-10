#-*- codeing = utf-8 -*-
#@Time: 2022/6/5 23:28
#@Author: 怪盗LLYL
#@File: auth.py
#@Software: PyCharm
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from myapp.utils.jwt_auth import parse_payload


class JwtQueryParamAuthentication(BaseAuthentication):
    """
    用户需要在url中通过参数进行传输token，例如：
    http://www.pythonav.com?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):
        token = request.query_params.get('token')
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (payload, token)

class JwtAuthorizationAuthentication(BaseAuthentication):
    """
    用户需要通过请求头的方式来进行传输token，例如：
    Authorization:jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """
    def authenticate(self, request):

        # 如果headerkey为auth - token，即headers = {'auth-token': '1234'}
        # 应该使用request.META.get("HTTP_AUTH_TOKEN")
        # 获取
        # headerkey中的小写转为大写，横线“-”转为下划线“_”, 并且加上前缀HTTP
        # 尤其注意headerkey中不应该包含
        # HTTP前缀，以及符号
        # "_", 否则会取不到对应的值
        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        if not auth:
            raise exceptions.AuthenticationFailed({'error': '未获取到Authorization请求头', 'status': False})
        if auth[0].lower() != 'jwt':
            raise exceptions.AuthenticationFailed({'error': 'Authorization请求头中认证方式错误', 'status': False})

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed({'error': "非法Authorization请求头", 'status': False})
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed({'error': "非法Authorization请求头", 'status': False})

        token = auth[1]
        result = parse_payload(token)
        if not result['status']:
            raise exceptions.AuthenticationFailed(result)
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (result, token)