from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Q 객체 임포트 추가
from django.utils import timezone
from django.http import HttpResponse
from .models import Event
from .forms import EventForm
import calendar

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Q 객체 임포트 추가
from django.utils import timezone
from django.http import HttpResponse
from .models import Event
from .forms import EventForm
import calendar

@login_required
def calendar_view(request, year=None, month=None):
    today = timezone.now()
    
    # 연도와 월이 전달되지 않았을 때 현재 연도와 월로 설정
    year = year or today.year
    month = month or today.month

    # 유효한 연도와 월인지 확인
    try:
        # GET 파라미터로 받은 값을 우선적으로 처리
        if 'year' in request.GET:
            year = int(request.GET.get('year', year))
        if 'month' in request.GET:
            month = int(request.GET.get('month', month))
        
        # 월이 유효하지 않으면 오류 반환
        if month < 1 or month > 12:
            raise ValueError("유효하지 않은 월입니다.")
    
    except ValueError:
        # 잘못된 파라미터 처리
        return HttpResponse("잘못된 연도나 월입니다.", status=400)

    # public=True인 일정 또는 본인이 작성한 일정만 필터링
    events = Event.objects.filter(
        start_date__year=year,
        start_date__month=month
    ).filter(Q(is_public=True) | Q(created_by=request.user))

    # 달력 데이터 생성 (일요일 시작)
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

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