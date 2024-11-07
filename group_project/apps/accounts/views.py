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
    if request.method == 'POST': # 제출된 경우
        form = AuthenticationForm(request, data=request.POST)  #  사용자명과 비밀번호가 올바른지 확인
        if form.is_valid(): #인증된 객체를 가져옴
            user = form.get_user() #사용자 객체를 가져옴
            auth_login(request, user) # 로그인 처리 
            return redirect('home')  # 로그인 후 홈으로 이동 
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

# Admin 유저만 접근 가능하도록 하는 데코레이터
def admin_required(view_func):
    # login_required와 user_passes_test 데코레이터를 사용하여,
    # 로그인한 유저가 관리자 (is_superuser=True) 인지 확인하는 데코레이터를 생성
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    # 접근 조건이 설정된 뷰 함수를 반환
    return decorated_view_func

# 사용자 목록을 보여주는 뷰 (Admin 유저만 접근 가능)
@admin_required
def user_list_view(request):
    # 모든 사용자 정보를 가져옴
    users = User.objects.all()
    # 'accounts/user_list.html' 템플릿을 사용하여 사용자 목록을 렌더링
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

# 사용자 수정 뷰 (Admin 유저만 접근 가능)
@admin_required
def edit_user_view(request, user_id):
    # 주어진 user_id에 해당하는 사용자를 가져오거나, 없으면 404 오류 반환
    user = get_object_or_404(User, id=user_id)
    # 요청 방식이 POST인지 확인 (즉, 폼이 제출된 경우)
    if request.method == 'POST':
        # 제출된 데이터와 함께 사용자 수정 폼을 초기화 (instance=user로 특정 사용자 정보 수정)
        form = CustomUserChangeForm(request.POST, instance=user)      
        # 폼 데이터가 유효한지 확인
        if form.is_valid():
            # 유효하다면 폼을 저장하여 사용자 정보를 업데이트
            form.save()
            # 성공 메시지를 추가하여 사용자에게 알림
            messages.success(request, '사용자 정보가 성공적으로 수정되었습니다.')
            # 사용자 목록 페이지로 리디렉션
            return redirect('user_list')
    # 요청 방식이 POST가 아닌 경우 (예: GET), 기존 사용자 데이터를 폼에 표시
    else:
        form = CustomUserChangeForm(instance=user)    
    # 사용자 수정 페이지를 렌더링하며, 폼과 사용자 정보를 전달
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