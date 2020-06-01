from django.conf import settings
from django.conf.urls import url
from .views import UserIndexView

urlpatterns = [
    # url(r"^search/$",  UserIndexView.as_view(), name="user_index"),
]