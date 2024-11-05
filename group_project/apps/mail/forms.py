# forms.py

from django import forms
from apps.accounts.models import CustomUser  # CustomUser 모델을 가져옵니다
from .models import Mail

class MailForm(forms.ModelForm):
    attachments = forms.FileField(required=False)
    
    # CustomUser를 선택할 수 있도록 설정
    recipient = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'recipient-select'}),
        required=True,
        label="받는 사람"
    )

    class Meta:
        model = Mail
        fields = ['recipient', 'cc', 'subject', 'body', 'attachments']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 6}),
        }

