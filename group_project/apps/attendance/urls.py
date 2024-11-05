from django.urls import path
from . import views

app_name = 'attendance'  # 또는 'messenger', 'mail'에 맞게 네임스페이스 정의

urlpatterns = [
    path('', views.index, name='index'),  # URL 패턴 정의
]