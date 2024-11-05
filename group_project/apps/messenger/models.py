from django.conf import settings
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='sent_messages', 
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='received_messages', 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # 메시지의 읽음 상태를 추적

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content[:20]}{"..." if len(self.content) > 20 else ""}'

    class Meta:
        ordering = ('-timestamp',)  # 메시지를 시간 역순으로 정렬
