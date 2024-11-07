from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.decorators import login_required

@login_required
def attendance_check(request):
    if request.method == 'POST':
        if 'check_in' in request.POST:
            Attendance.objects.create(user=request.user, attendance_time=timezone.now())
            return redirect('attendance:index')  # 출석 체크 후 인덱스 페이지로 리다이렉트
        elif 'check_out' in request.POST:
            attendance_record = Attendance.objects.filter(user=request.user, leave_time__isnull=True).last()
            if attendance_record:
                attendance_record.leave_time = timezone.now()
                attendance_record.save()
                return redirect('attendance:index')  # 퇴근 체크 후 인덱스 페이지로 리다이렉트

    # 지난 7일간 출석 기록 가져오기
    week_attendance = Attendance.objects.filter(user=request.user, attendance_time__gte=timezone.now() - timezone.timedelta(days=7))
    
    return render(request, 'attendance/home.html', {
        'week_attendance': week_attendance
    })

@login_required
def home(request):
    return render(request, 'attendance/home.html')  # home.html 템플릿 파일을 렌더링




