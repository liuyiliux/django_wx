#-*- codeing = utf-8 -*-
#@Time: 2022/5/30 20:33
#@Author: 怪盗LLYL
#@File: auth_utils.py
#@Software: PyCharm
import hashlib
from django_wx import  settings

def password_encry(psw):
    USER_PWS = []
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(psw.encode('utf-8'))
    encry_psw = obj.hexdigest()
    return encry_psw
if __name__ == '__main__':
    print(password_encry('aaaaaa'))