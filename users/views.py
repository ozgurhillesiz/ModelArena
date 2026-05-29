from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from models_app.models import UserFavorite, Review, Notification, UserActivity

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': True})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    favorites = UserFavorite.objects.filter(user=request.user).select_related('model')
    reviews = Review.objects.filter(user=request.user).select_related('model').order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    activities = UserActivity.objects.filter(user=request.user).select_related('model')[:20]

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            profile = request.user.profile
            profile.avatar = request.FILES['avatar']
            profile.save()
            messages.success(request, 'Profil fotoğrafın güncellendi!')
            return redirect('profile')
        if 'bio' in request.POST:
            profile = request.user.profile
            profile.bio = request.POST.get('bio', '')
            profile.save()
            messages.success(request, 'Hakkımda bilgisi güncellendi!')
            return redirect('profile')

    return render(request, 'users/profile.html', {
        'favorites': favorites,
        'reviews': reviews,
        'notifications': notifications,
        'unread_count': unread_count,
        'activities': activities,
    })

@login_required
def mark_notification_read(request, pk):
    try:
        notif = Notification.objects.get(pk=pk, user=request.user)
        notif.is_read = True
        notif.save()
    except:
        pass
    return redirect('profile')

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('profile')

@login_required
def notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})