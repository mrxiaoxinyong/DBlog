# encoding:utf-8
import uuid
import os
import markdown
from DjangoUeditor.models import UEditorField
from blog_module.utils import getImagePath, getUploadPath
from blog_module.choices import SelectContentChoices, PublishTypeChoices
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from user_module.models import UserInfo


# student.photo_url
# 文章
# 标题
# markdown内容
# ueditor富文本内容
# 选择哪种文本
# 标签
# 分类
# 类型（原创，转载，翻译）
# 资源信息（图片，文件等）
# 发布形式（公开，秘密，粉丝, vip)可见
# 阅读人数
# 评论人数
# 创建时间
# 更新时间
# 标签表
# 名称
# 分类表
# 名称
# 描述
# 图片路径


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    try:
        filename = '{0}.{1}'.format(instance.name, ext)
        return os.path.join("blog/catagory/" + instance.author.username, filename)  # 系统路径分隔符差异，增强代码重用性
    except AttributeError:
        filename = '{0}.{1}'.format(instance.title, ext)
        return os.path.join("blog/article/" + instance.author.username, filename)  # 系统路径分隔符差异，增强代码重用性


class Label(TimeStampedModel):
    name = models.CharField(verbose_name="label", unique=True, max_length=50, db_index=True, null=True, blank=True)

    name_en = models.CharField(verbose_name="label_en", unique=True, max_length=50, db_index=True, null=True,
                               blank=True)

    publish = models.BooleanField(verbose_name="publish", default=False)

    class Meta:
        index_together = [
            ["name", "publish"],
            ["name_en", "publish"],
        ]

    def __str__(self):
        return self.name


class UserCatagory(TimeStampedModel):
    author = models.ForeignKey(verbose_name="user", to=UserInfo, related_name="user_catalog", db_index=True)
    name = models.CharField(verbose_name="catalog_name", max_length=50, db_index=True, null=True, blank=True)
    name_en = models.CharField(verbose_name="catalog_name_en", max_length=50, db_index=True, null=True,
                               blank=True)  # 暂时先不用
    describe = models.TextField(verbose_name="describe", null=True, blank=True)
    payment = models.BooleanField(verbose_name="required_pay", default=False)  # 暂时不用这个功能， 先记录下来
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    image_295_413 = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(295, 413)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    image_90_90 = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(90, 90)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )

    class Meta:
        unique_together = (('author', 'name'),)
        index_together = [
            ['author', 'name'],
        ]

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.MEDIA_URL + "blog/catagory/default.jpg"

    @property
    def image_295_413_url(self):
        if self.photo_295_413 and hasattr(self.photo_295_413, 'url'):
            return self.photo_295_413.url
        else:
            return settings.MEDIA_URL + "blog/catagory/default.jpg"

    @property
    def image_90_90_url(self):
        if self.image_90_90 and hasattr(self.image_90_90, 'url'):
            return self.image_90_90.url
        else:
            return settings.MEDIA_URL + "blog/catagory/default.jpg"


class ArticleMixin(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    title = models.CharField(verbose_name="title", max_length=255, db_index=True)
    content_mkd = models.TextField(verbose_name="markdown", null=True, blank=True)
    content_udt = UEditorField(verbose_name='ueditor', width=600, height=300, toolbars="full", imagePath=getImagePath(),
                               filePath=getUploadPath(),
                               upload_settings={"imageMaxSize": 1204000}, settings={}, null=True, blank=True)

    select_content = models.IntegerField(default=1, choices=SelectContentChoices.choices,
                                         help_text=_("content type of select"))
    publish_type = models.IntegerField(verbose_name="publish_type", default=1, choices=PublishTypeChoices.choices)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    image_295_413 = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(295, 413)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    image_90_90 = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(90, 90)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )

    class Meta:
        abstract = True

    @property
    def content(self):
        print(self.select_content)
        if self.select_content:
            return self.content_udt
        else:
            return self.markdown_to_html(self.content_mkd)

    def markdown_to_html(self, content):
        content = markdown.markdown(content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
        return content

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.MEDIA_URL + "blog/article/default.jpg"

    @property
    def image_295_413_url(self):
        if self.photo_295_413 and hasattr(self.photo_295_413, 'url'):
            return self.photo_295_413.url
        else:
            return settings.MEDIA_URL + "blog/catagory/default.jpg"

    @property
    def image_90_90_url(self):
        if self.image_90_90 and hasattr(self.image_90_90, 'url'):
            return self.image_90_90.url
        else:
            return settings.MEDIA_URL + "blog/catagory/default.jpg"


class DraftArticle(ArticleMixin):
    author = models.ForeignKey(verbose_name="user", to=UserInfo, related_name="draft_article", db_index=True)
    label = models.ManyToManyField(verbose_name="label", to=Label, related_name="draft_article",  null=True, blank=True)
    category = models.ForeignKey(verbose_name="category", to=UserCatagory, related_name="draft_article")
    is_active = models.BooleanField(verbose_name="is_active", default=True, db_index=True)

    class Meta:
        index_together = [
            ['author', 'title'],
            ['author', 'publish_type'],
            ['author', 'is_active'],
        ]

    def publish(self):
        PublishArticle.objects.update_or_create(
            author=self.author,
            uuid=self.uuid,
            defaults={
                "title": self.title,
                "content_mkd": self.content_mkd,
                "content_udt": self.content_udt,
                "select_content": self.select_content,
                "label": self.label,
                "category": self.category,
                "publish_type": self.publish_type
            }
        )


class PublishArticle(ArticleMixin):
    author = models.ForeignKey(verbose_name="user", to=UserInfo, related_name="article", db_index=True)
    label = models.ManyToManyField(verbose_name="label", to=Label, related_name="article", null=True, blank=True)
    category = models.ForeignKey(verbose_name="category", to=UserCatagory, related_name="article")
    publish_status = models.BooleanField(verbose_name="publish_status", default=0)

    class Meta:
        index_together = [
            ['author', 'title'],
            ['author', 'publish_type'],
            ['author', 'publish_status'],
            ['author', 'publish_type', 'publish_status'],
        ]


class TrafficMixin(TimeStampedModel):
    number = models.IntegerField(verbose_name="reads", default=0)


class TrafficArticle(TrafficMixin):
    article = models.OneToOneField(verbose_name="article", to=PublishArticle, related_name="tarffic")


class TrafficCategory(TrafficMixin):
    category = models.OneToOneField(verbose_name="article", to=UserCatagory, related_name="tarffic")
