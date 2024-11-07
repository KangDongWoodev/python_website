# apps/mail/views.py

from django.shortcuts import render, redirect
from .forms import MailForm
from django.shortcuts import render, get_object_or_404
from .models import Mail
from django.shortcuts import render, redirect
from .models import Mail

def mail_list(request):
    # GET 요청에서 'filter' 값을 가져오고, 없으면 기본값으로 'received' 설정
    filter_type = request.GET.get('filter', 'received')

    # 필터에 따라 메일을 선택
    if filter_type == 'received':
        # 받은 메일: 사용자가 수신자인 메일만 선택
        mails = Mail.objects.filter(recipient=request.user)
    elif filter_type == 'sent':
        # 보낸 메일: 사용자가 발신자인 메일만 선택
        mails = Mail.objects.filter(sender=request.user)
    else:
        # 잘못된 필터 값일 경우 빈 결과 반환
        mails = Mail.objects.none()

    # 템플릿에 전달할 데이터를 사전 형태로 저장
    context = {
        'mails': mails,         # 필터링된 메일 목록
        'filter': filter_type,  # 현재 필터 유형 ('received' 또는 'sent')
    }
    
    # 'new_mail_list.html' 템플릿을 렌더링하면서 메일 목록과 필터 정보를 전달
    return render(request, 'mail/new_mail_list.html', context)


def compose_mail(request):
    if request.method == "POST":
        form = MailForm(request.POST, request.FILES)  # request.FILES 추가
        if form.is_valid():
            mail = form.save(commit=False)
            mail.sender = request.user  # 현재 로그인한 사용자를 발신자로 설정
            mail.save()
            form.save_m2m()  # Many-to-many 관계 필드를 저장

            # 첨부 파일 저장
            for file in request.FILES.getlist('attachments'):
                mail.attachments.create(file=file)

            return redirect('mail:mail_list')  # 메일 목록 페이지로 이동
    else:
        form = MailForm()

    return render(request, 'mail/compose_mail.html', {'form': form})

def send_mail(request):
    # 요청 방식이 POST인지 확인 (즉, 메일 작성 폼이 제출된 경우)
    if request.method == 'POST':
        # 제출된 데이터와 파일을 사용해 메일 작성 폼을 초기화
        form = MailForm(request.POST, request.FILES)
        # 폼이 유효한지 확인
        if form.is_valid():
            # 임시로 폼 데이터를 저장하여 메일 객체 생성
            mail = form.save(commit=False)
            # 이 메일을 '보낸 메일'로 표시
            mail.is_sent = True
            # 메일 객체를 DB에 저장
            mail.save()
            # 첨부 파일 목록을 가져옴
            attachments = request.FILES.getlist('attachments')
            # 각 첨부 파일에 대해 처리 (첨부 파일 로직은 여기에 추가)
            for file in attachments:
                # 첨부 파일 처리 로직을 여기에 추가
                pass 
            # 메일 목록 페이지로 이동
            return redirect('mail:mail_list')
    
    # 요청 방식이 POST가 아닌 경우 (예: GET), 빈 메일 작성 폼을 초기화
    else:
        form = MailForm()
    
    # 메일 작성 페이지를 이동하며, 폼을 전달
    return render(request, 'compose_mail.html', {'form': form})


def mail_detail(request, pk):
    # 주어진 pk (기본 키)에 해당하는 메일 객체를 가져오고, 없으면 404 오류를 반환
    mail = get_object_or_404(Mail, pk=pk) 
    # 페이지에 전달할 데이터를 사전 형태로 저장
    context = {
        'mail': mail,  # 메일 객체를 추가하여 html 페이지에 사용
    }
    # 'mail_detail.html' 세부메일 내역 보여주면서 메일 데이터를 전달
    return render(request, 'mail/mail_detail.html', context)