# models.py

from django.db import models
from apps.accounts.models import CustomUser  # CustomUser 모델 가져오기

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    mail = models.ForeignKey('Mail', on_delete=models.CASCADE, related_name='attachments')

class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_mails')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_mails')
    cc = models.CharField(max_length=255, blank=True, default="")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
