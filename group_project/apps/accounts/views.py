from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()  # CustomUser 모델을 가져옵니다

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # 로그인 후 홈으로 리다이렉트
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

# Admin 유저만 접근 가능하도록 하는 데코레이터
def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

# 사용자 목록 뷰
@admin_required
def user_list_view(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

# 사용자 생성 뷰
@admin_required
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '사용자가 성공적으로 생성되었습니다.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/create_user.html', {'form': form})

# 사용자 수정 뷰
@admin_required
def edit_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '사용자 정보가 성공적으로 수정되었습니다.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'accounts/edit_user.html', {'form': form, 'user': user})

# 사용자 삭제 뷰
@admin_required
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, '사용자가 성공적으로 삭제되었습니다.')
        return redirect('user_list')
    return render(request, 'accounts/delete_user.html', {'user': user})