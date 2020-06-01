# _*_ encoding:utf-8 _*_
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户：划分角色
    """
    real_name = models.CharField(max_length=50, verbose_name=u"真实姓名", default="")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"手机号")
    image = models.ImageField(upload_to="img/", default=u"img/default.png", max_length=100, verbose_name=u"头像", null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.real_name
