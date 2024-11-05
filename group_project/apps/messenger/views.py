from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()

@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messenger/chat_list.html', {'users': users})

@login_required
def chat_room(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    messages.update(is_read=True)

    available_users = User.objects.exclude(id=request.user.id)

    return render(request, 'messenger/chat_room.html', {
        'receiver': receiver,
        'messages': messages,
        'users': available_users
    })