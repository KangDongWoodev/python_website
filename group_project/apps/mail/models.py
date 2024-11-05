# models.py

from django.db import models
from apps.accounts.models import CustomUser  # CustomUser 모델 가져오기

class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_mails')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_mails')
    cc = models.CharField(max_length=255, blank=True, default="")  # 기본값 추가
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
