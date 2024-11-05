from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Event
from .forms import EventForm
import calendar

def calendar_view(request, year=None, month=None):
    today = timezone.now()
    
    # 현재 연도와 월을 기본값으로 설정
    year = year or today.year
    month = month or today.month

    # 유효한 연도와 월인지 확인
    try:
        year = int(year)
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError
    except (ValueError, TypeError):
        return HttpResponse("잘못된 연도나 월입니다.", status=400)

    # 달력 데이터 생성 (일요일 시작)
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 해당 월의 모든 이벤트를 가져옵니다
    events = Event.objects.filter(start_date__year=year, start_date__month=month)

    # 날짜별 이벤트를 매핑
    days = {day: [] for day in range(1, 32)}
    for event in events:
        day = event.start_date.day
        days[day].append(event)

    # 달력의 각 주와 일 구조 생성
    calendar_weeks = []
    for week in month_days:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append({
                    'day': None,
                    'events': []
                })
            else:
                week_days.append({
                    'day': day,
                    'events': days.get(day, [])
                })
        calendar_weeks.append(week_days)

    context = {
        'year': year,
        'month': month,
        'calendar_weeks': calendar_weeks,
        'year_range': range(today.year - 5, today.year + 6),
        'month_range': range(1, 13),
    }

    return render(request, 'scheduler/calendar.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'scheduler/event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # 현재 로그인한 사용자로 설정
            event.save()
            return redirect('scheduler:calendar')  # 저장 후 달력 페이지로 리디렉션
    else:
        form = EventForm()

    context = {
        'form': form,
    }
    return render(request, 'scheduler/event_form.html', context)