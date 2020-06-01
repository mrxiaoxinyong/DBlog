from django.conf import settings
from django.conf.urls import url
from .views import UserIndexView

urlpatterns = [
    url(r"^index/$",  UserIndexView.as_view(), name="user_index"),
]