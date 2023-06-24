import random
import re

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import DB_weatherinfo_base, DB_weatherinfo_all, DB_user, DB_href
from myapp.utils.auth import JwtAuthorizationAuthentication
from myapp.utils.auth_utils import password_encry, save_wxuser
from myapp.utils.jwt_auth import create_token, parse_payload
from myapp.utils.sendemail import MyEmail
from myapp.utils.weatherInfo_utils import Gaode_tianqi
import datetime

from myapp.utils.wxutils import jscode2session


class get_weatherinfo_base(APIView):
    authentication_classes = [JwtAuthorizationAuthentication, ]
    def get(self, request, *args, **kwargs):
        city = self.kwargs['city']
        tianqi = Gaode_tianqi(city).get_weatherinfo_base()
        update_or_create_weatherinfo_base(city, tianqi)
        return Response({"datas":tianqi})
    def post(self, request, *args, **kwargs):
        city = self.kwargs['city']
        tianqi = Gaode_tianqi(city).get_weatherinfo_base()
        update_or_create_weatherinfo_base(city, tianqi)
        return Response({"datas":tianqi})
class register(APIView):
    def post(self, request, *args, **kwargs):
        # 如果headerkey为auth - token，即headers = {'auth-token': '1234'}
        # 应该使用request.META.get("HTTP_AUTH_TOKEN")
        # 获取 headerkey中的小写转为大写，横线“-”转为下划线“_”, 并且加上前缀HTTP
        # 尤其注意headerkey中不应该包含HTTP前缀，以及符号"_", 否则会取不到对应的值
        # params用于获取字符串，
        # data：用于获取正文，
        # post方法两个参数都可以使用，get方法只能使用params
        # print(request.META.get("HTTP_AUTH_TOKE",'321'))
        username = request.data.get("username",None)
        re_str = re.compile("^[a-zA-Z0-9_-]{3,15}$")
        if re_str.search(username):
            pass
        else:
            payload = {'status': "299", 'error': "用户名格式不正确"}
            return Response(payload)
        password = request.data.get("password",None)
        if re_str.search(password):
            pass
        else:
            payload = {'status': "299", 'error': "密码格式不正确"}
            return Response(payload)
        email = request.data.get("email",None)
        emailcode = request.data.get("emailcode",None)
        if username == None or password == None or email == None:
            payload = {'status': "204", 'error': "参数为空"}
            return Response(payload)
        elif DB_user.objects.filter(username=username):
            payload = {'status': "202", 'error': "用户名已存在"}
            return Response(payload)
        elif DB_user.objects.filter(email=email):
            payload = {'status': "205", 'error': "邮箱已存在"}
            return Response(payload)
        if emailcode != request.session.get('emailcode', None) or  email != request.session.get('email', None):
            print( request.session.get('emailcode', None))
            print( request.session.get('email', None))
            payload={'status': "203", 'error': "验证码不正确"}
            return Response(payload)
        else:
            try:
                password = password_encry(password)
                DB_user.objects.create(username=username,password=password,email=email,type=0)
                payload = {'status': "200", 'message': "注册成功"}
            except Exception as e:
                print(e.__str__())
                payload = {'status': "299", 'error': "其他错误"}
                return Response(payload)
        return Response(payload)
class login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username",None)
        password = request.data.get("password",None)
        if len(username) == 0 or len(password) == 0 :
            payload = {'status': "204", 'error': "参数为空"}
            return Response(payload)
        else:
            try:
                password = password_encry(password)
                if len(DB_user.objects.filter(username=username, password=password))==0:
                    payload = {'status': "206", 'error': "用户名或者密码错误"}
                    return Response(payload)
                else:
                    userInfo = {"username":username}
                    payload = userInfo
                    token = create_token(payload)
                    return Response({'status': "200", 'userInfo': payload,'Token': token},headers={"Token":token,"Access-Control-Expose-Headers":"Token"})
            except Exception as e:
                print(e.__str__())
                payload = {'status': "299", 'error': "其他错误"}
                return Response(payload)
# 自定义的ExpiringTokenAuthentication认证方式
class wx_login(APIView):
    def post(self, request, *args, **kwargs):
        """ 用户登录 """
        # params用于获取字符串，
        # data：用于获取正文，
        # post方法两个参数都可以使用，get方法只能使用params
        code = request.data.get('code')
        # 检测用户和密码是否正确，此处可以在数据进行校验。
        if code:
            # 存在code
            wxdata = jscode2session(code)
            if wxdata.get('status'):
                userInfo = request.data.get('userInfo')
                userInfo['openid'] = wxdata.get('data')['openid']
                userInfo['unionid'] = wxdata.get('data')['unionid']
                save_wxuser(userInfo) #保存用户
                payload = userInfo
                token = create_token(payload) #创建token
                return Response({'status': "True", 'userInfo': payload}, headers={'token': token})
            else:
                return Response({'status': "False", 'error': wxdata.get('error')})
        return Response({'status': "False", 'error': '不存在code'})
class logintoken(APIView):
    def post(self, request, *args, **kwargs):
        """ 用户登录 """
        # params用于获取字符串，
        # data：用于获取正文，
        # post方法两个参数都可以使用，get方法只能使用params
        # request.data{'code':'0042e209909bdc1de90a985721788fba','userInfo': {'avatarUrl': 'https://thirdqq.qlogo.cn/qqapp/1111606452/8ABBB9AD27105F660A44709478527506/100','nickName': 'test'}}
        token = request.data.get('token')
        # 检测用户和密码是否正确，此处可以在数据进行校验。
        if token:
            # 存在token
            payload = parse_payload(token)
            # {'status': True, 'data': {'avatarUrl': 'https://thirdqq.qlogo.cn/qqapp/1111606452/8ABBB9AD27105F660A44709478527506/100','nickName': '\uf8ff', 'openid': '8ABBB9AD27105F660A44709478527506','unionid': 'UID_264350906702A439A7FAA9D573B40B1F', 'exp': 1651342555}, 'error': None}
            if payload.get('status'):
                userInfo = payload.get('data')
                userInfo.pop('exp')
                payload = userInfo
                token = create_token(payload)
                return Response({'status': "True", 'userInfo': payload}, headers={'token': token})
            else:
                return Response({'status': "False", 'error': payload.get('error')})
        return Response({'status': "False", 'error': '不存在token'})


class sendcode(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        code_list = []
        for i in range(6):  # 控制验证码的位数
            state = random.randint(1, 3)  # 生成状态码
            if state == 1:
                first_kind = random.randint(65, 90)  # 大写字母
                random_uppercase = chr(first_kind)
                code_list.append(random_uppercase)
            elif state == 2:
                second_kinds = random.randint(97, 122)  # 小写字母
                random_lowercase = chr(second_kinds)
                code_list.append(random_lowercase)
            elif state == 3:
                third_kinds = random.randint(0, 9)
                code_list.append(str(third_kinds))
        emailcode = "".join(code_list)
        print(emailcode)
        myemail = MyEmail()
        myemail.sendemail(emailcode,email)
        request.session['emailcode'] = emailcode
        request.session['email'] = email
        payload={'status': "200", 'message': "发送成功"}
        return Response(payload)


def update_or_create_weatherinfo_base(city,tianqi):
    try:
        lives = tianqi['lives'][0]
        city = lives['city']
        province = lives['province']
        weather = lives['weather']
        temperature = lives['temperature']
        winddirection = lives['winddirection']
        windpower = lives['windpower']
        humidity = lives['humidity']
        reporttime = lives['reporttime']
        reporttime = datetime.datetime.strptime(reporttime, '%Y-%m-%d %H:%M:%S')

        obj, created = DB_weatherinfo_base.objects.update_or_create(city=city, defaults={"province": province, "weather": weather,
                                                                                 "temperature": temperature,
                                                                                 "winddirection": winddirection,
                                                                                 "windpower": windpower,
                                                                                 "humidity": humidity,
                                                                                 "reporttime": reporttime})
        return {'status': True}
    except Exception as e:
        print(e.__str__())
        return {'status': False}

class get_weatherinfo_all(APIView):
    # authentication_classes = [JwtAuthorizationAuthentication, ]
    def get(self, request, *args, **kwargs):
        city = self.kwargs['city']
        tianqi = Gaode_tianqi(city).get_weatherinfo_all()
        update_or_create_weatherinfo_all(city, tianqi)
        return Response({"datas":tianqi})

def update_or_create_weatherinfo_all(city,tianqi):
    forecasts  = tianqi['forecasts'][0]
    casts = forecasts['casts']
    try:
        for cast in casts:
            city = forecasts['city']
            province = forecasts['province']
            date = cast['date']
            week = cast['week']
            dayweather = cast['dayweather']
            nightweather = cast['nightweather']
            daytemp = cast['daytemp']
            nighttemp = cast['nighttemp']
            daywind = cast['daywind']
            nightwind = cast['nightwind']
            daypower = cast['daypower']
            nightpower = cast['nightpower']
            reporttime = forecasts['reporttime']
            reporttime = datetime.datetime.strptime(reporttime, '%Y-%m-%d %H:%M:%S')
            obj, created = DB_weatherinfo_all.objects.update_or_create( defaults={"province": province, "week": week,
                                                                                     "dayweather": dayweather,
                                                                                     "nightweather": nightweather,
                                                                                     "daytemp": daytemp,
                                                                                     "nighttemp": nighttemp,
                                                                                     "daywind": daywind,
                                                                                     "nightwind": nightwind,
                                                                                     "daypower": daypower,
                                                                                     "nightpower": nightpower,
                                                                                     "reporttime": reporttime
                                                                                                       },city=city,date=date)
        return {'status': True}
    except Exception as e:
        print(e.__str__())
        return {'status': False}

class geturl(APIView):
    # authentication_classes = [JwtAuthorizationAuthentication, ]
    def get(self, request, *args, **kwargs):
        index = request.GET.get("event",None)
        if index ==None or len(index)==0:
            all_href = DB_href.objects.all().values()
        else:
            all_href = DB_href.objects.filter(name__icontains=index).values()
        return Response({"all_href":all_href})

class add_href(APIView):
    authentication_classes = [JwtAuthorizationAuthentication, ]
    def post(self, request, *args, **kwargs):
        try:
            new_link_name = request.data['new_link_name']
            new_link_url = request.data['new_link_url']
            username = request.user['data']['username']
            href = DB_href.objects.create(name=new_link_name, url=new_link_url, author=username)
            href.save()
            return Response({'status': "200"})
        except Exception as e:
            print(e.__str__())
            payload = {'status': "299", 'error':e.__str__()}
            return Response(payload)

class delete_href(APIView):
    authentication_classes = [JwtAuthorizationAuthentication, ]
    def post(self, request, *args, **kwargs):
        try:
            id = request.data['id']
            href = DB_href.objects.filter(id=id)
            href.delete()
            return Response({'status': "200"})
        except Exception as e:
            print(e.__str__())
            payload = {'status': "299", 'error': e.__str__()}
            return Response(payload)
