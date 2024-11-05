# apps/mail/views.py

from django.shortcuts import render, redirect
from .forms import MailForm
from .models import Mail
from django.shortcuts import render, redirect
from .models import Mail

def mail_list(request):
    filter_type = request.GET.get('filter', 'received')  # 기본값은 'received'로 설정

    if filter_type == 'received':
        mails = Mail.objects.filter(recipient=request.user)
    elif filter_type == 'sent':
        mails = Mail.objects.filter(sender=request.user)
    else:
        mails = Mail.objects.none()  # 기본적으로 빈 쿼리셋

    context = {
        'mails': mails,
        'filter': filter_type,
    }
    return render(request, 'mail/new_mail_list.html', context)

def compose_mail(request):
    if request.method == "POST":
        form = MailForm(request.POST, request.FILES)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.sender = request.user  # 현재 로그인한 사용자를 발신자로 설정
            mail.save()
            form.save_m2m()  # Many-to-many 관계 필드를 저장
            return redirect('mail:mail_list')  # 메일 목록 페이지로 이동
        else:
            # 폼이 유효하지 않은 경우 오류 메시지 출력
            print(form.errors)
    else:
        form = MailForm()

    return render(request, 'mail/compose_mail.html', {'form': form})

def send_mail(request):
    if request.method == 'POST':
        form = MailForm(request.POST, request.FILES)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.is_sent = True  # Mark this mail as sent
            mail.save()
            attachments = request.FILES.getlist('attachments')
            for file in attachments:
                # Attachments processing logic here
                pass
            return redirect('mail:mail_list')
    else:
        form = MailForm()
    
    return render(request, 'compose_mail.html', {'form': form})

def mail_detail(request, mail_id):
    mail = get_object_or_404(Mail, id=mail_id)
    return render(request, 'mail_detail.html', {'mail': mail})