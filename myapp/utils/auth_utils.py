#-*- codeing = utf-8 -*-
#@Time: 2022/5/30 20:33
#@Author: 怪盗LLYL
#@File: auth_utils.py
#@Software: PyCharm
import hashlib
from django_wx import  settings
from myapp.models import DB_user


def password_encry(psw):
    USER_PWS = []
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(psw.encode('utf-8'))
    encry_psw = obj.hexdigest()
    return encry_psw
def save_wxuser(userInfo):
    try:
        openid = userInfo['openid']
        unionid = userInfo['unionid']
        nick_name = userInfo['nickName']
        avatar_url = userInfo['avatarUrl']
        obj, created = DB_user.objects.update_or_create(openid=openid,defaults={"unionid":unionid,"nick_name":nick_name,"avatar_url":avatar_url,"type":"1"})
        return {'status': True}
    except Exception as e:
        print(e.__str__())
        return {'status': False}

if __name__ == '__main__':
    print(password_encry('aaaaaa'))