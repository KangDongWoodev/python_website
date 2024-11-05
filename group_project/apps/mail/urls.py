# apps/mail/urls.py
# urls.py

from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('mail_list/', views.mail_list, name='mail_list'),
    path('compose/', views.compose_mail, name='compose_mail'),
    path('detail/<int:pk>/', views.mail_detail, name='mail_detail'),
]
