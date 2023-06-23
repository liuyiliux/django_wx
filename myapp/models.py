from django.utils import timezone
from django.db import models
# Create your models here.
class DB_weatherinfo_base(models.Model):
    city = models.CharField(primary_key=True,verbose_name='地市',null=False ,blank=False,max_length=5)
    province = models.CharField(verbose_name='省份',null=False ,blank=False,max_length=5)
    weather =  models.CharField(verbose_name='天气现象',null=False ,blank=False,max_length=5)
    temperature =  models.CharField(verbose_name='实时气温',null=False ,blank=False,max_length=5)
    winddirection =  models.CharField(verbose_name='风向',null=False ,blank=False,max_length=5)
    windpower =  models.CharField(verbose_name='风力级别',null=False ,blank=False,max_length=5)
    humidity =  models.CharField(verbose_name='空气湿度',null=False ,blank=False,max_length=3)
    reporttime =  models.DateTimeField(verbose_name='数据发布的时间',default=timezone.now)
    # 设置联合主键
    class Meta:
        verbose_name_plural ="当前天气"
    def __str__(self):
        return str(self.city+str(self.reporttime)+self.weather)
class DB_weatherinfo_all(models.Model):
    city = models.CharField(verbose_name='地市',null=False ,blank=False,max_length=5)
    province = models.CharField(verbose_name='省份',null=False ,blank=False,max_length=5)
    date = models.CharField(verbose_name='日期',null=False ,blank=False,max_length=10)
    week = models.CharField(verbose_name='星期',null=False ,blank=False,max_length=1)
    dayweather =  models.CharField(verbose_name='白天天气',null=False ,blank=False,max_length=5)
    nightweather =  models.CharField(verbose_name='晚上天气',null=False ,blank=False,max_length=5)
    daytemp =  models.CharField(verbose_name='白天气温',null=False ,blank=False,max_length=5)
    nighttemp =  models.CharField(verbose_name='晚上气温',null=False ,blank=False,max_length=5)
    daywind =  models.CharField(verbose_name='白天风向',null=False ,blank=False,max_length=5)
    nightwind =  models.CharField(verbose_name='晚上风向',null=False ,blank=False,max_length=5)
    daypower =  models.CharField(verbose_name='白天风力',null=False ,blank=False,max_length=5)
    nightpower =  models.CharField(verbose_name='晚上风力',null=False ,blank=False,max_length=5)
    reporttime =  models.DateTimeField(verbose_name='数据发布的时间',default=timezone.now)
    # 设置联合主键
    class Meta:
        verbose_name_plural ="未来天气"
        unique_together=('city','date')
    def __str__(self):
        return str(self.city+self.date+self.dayweather)
class DB_user(models.Model):
    username = models.CharField('用户名', null=True ,blank=True,max_length=32)
    password = models.CharField('密码', null=True ,blank=True,max_length=32)
    email = models.CharField('邮箱',max_length=30 , null=True ,blank=True)
    openid = models.CharField('微信的openid',null=True ,blank=True,max_length=32)
    unionid = models.CharField('微信的unionid',max_length=36 , null=True ,blank=True)
    nickname = models.CharField('微信昵称',max_length=30 , null=True ,blank=True)
    province = models.CharField('省份',max_length=10 , null=True ,blank=True)
    city = models.CharField('地市',max_length=10 , null=True ,blank=True)
    country = models.CharField('国家',max_length=10 , null=True ,blank=True)
    avatarurl = models.CharField('头像url',max_length=1000 , null=True ,blank=True,)
    sex = models.CharField('性别',max_length=1 ,null=True ,blank=True)
    qq = models.CharField('qq',max_length=15 ,null=True ,blank=True)
    weixin = models.CharField('微信号',max_length=20 ,null=True ,blank=True)
    nick_name = models.CharField('微信名',max_length=20 ,null=True ,blank=True)
    phone = models.CharField('手机号',max_length=11 , null=True ,blank=True)
    avatar_url = models.CharField('头像url',max_length=1000 , null=True ,blank=True)
    type = models.CharField('用户类型(0:网站，1：微信,2：qq',max_length=1 , null=True ,blank=True)
    def __str__(self):
        return str(self.username)
class DB_href(models.Model):
    name = models.CharField(max_length=30 , null=True ,blank=True,default='空')
    url = models.CharField(max_length=1000 , null=True ,blank=True,default='空')
    author =  models.CharField('作者',max_length=50,blank=True,null=True,default='')

    def __str__(self):
        return str(self.name)