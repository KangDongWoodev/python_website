from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, home_view, create_user_view, user_list_view, edit_user_view, delete_user_view

urlpatterns = [
    path('login/', login_view, name='login'), #로그인 접근
    path('home/', home_view, name='home'),
    path('users/', user_list_view, name='user_list'),  # 사용자 목록 페이지
    path('create_user/', create_user_view, name='create_user'),
    path('edit_user/<int:user_id>/', edit_user_view, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user_view, name='delete_user'),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),  # 로그아웃 URL 추가
]