from django.urls import path
from .views import attendance_check, home

app_name = 'attendance'  # 여기에 app_name을 추가해야 합니다.

urlpatterns = [
    path('', home, name='index'),  # 홈 페이지의 URL 패턴
    path('check/', attendance_check, name='attendance_check'),  # 출석 체크 페이지
]
