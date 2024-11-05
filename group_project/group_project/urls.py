# group_project/urls.py

from django.contrib import admin
from django.urls import path, include
from apps.accounts import views as accounts_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.login_view, name='home'),  # 메인 홈페이지를 home_view로 설정
    path('accounts/', include('apps.accounts.urls')),  # accounts 앱의 URL 연결
    path('attendance/', include('apps.attendance.urls')),  # 출석 앱의 URL 연결
    path('messenger/', include('apps.messenger.urls', namespace='messenger')),  # 네임스페이스 설정
    path('scheduler/', include('apps.scheduler.urls')),  # 일정 앱의 URL 연결
    path('mail/', include('apps.mail.urls')),  # 메일 앱의 URL 연결
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),  # 로그아웃 후 로그인 페이지로 리디렉트
]