# apps/attendance/models.py
from django.db import models
from django.conf import settings  # 이 줄을 추가
from django.utils import timezone
from django.contrib.auth import get_user_model

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.attendance_time} - {self.leave_time}"

    @property
    def is_late(self):
        if self.attendance_time and self.attendance_time.time() > timezone.datetime.time(9, 0):
            return True
        return False

    @property
    def is_working_hours(self):
        if self.attendance_time and self.leave_time:
            return self.attendance_time.date() == timezone.now().date() and self.leave_time > self.attendance_time
        return False
