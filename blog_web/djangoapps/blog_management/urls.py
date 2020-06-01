from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from .views import (
    BlogManageView,
    BlogEditView,
    BlogDetailView,
    BlogEditMarkdownView,
    BlogArticleView,
    CatalogEditView
)

router = SimpleRouter()
router.register(r'^article', BlogArticleView, base_name='article')
urlpatterns = router.urls

UUID_PATTERN = r'(?P<article_id>[a-zA-Z0-9\-]{30,40})'

urlpatterns += [
    url(r"^manage/$",  BlogManageView.as_view(), name="manage"),
    url(r"^edit/$",  BlogEditView.as_view(), name="edit"),
    url(r"^detail/{}$".format(UUID_PATTERN),  BlogDetailView.as_view(), name="detail"),
    url(r"^edit/markdown/$",  BlogEditMarkdownView.as_view(), name="markdown"),
    url(r"^catalog/edit$",  CatalogEditView.as_view(), name="catalog_edit"),

]