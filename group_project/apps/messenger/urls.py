from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('room/<int:user_id>/', views.chat_room, name='chat_room'),  # 수정된 URL 패턴
]