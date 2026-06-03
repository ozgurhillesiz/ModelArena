"""
ModelArena - Kullanıcı View'ları
=================================
Kayıt, giriş, çıkış, profil yönetimi, hesap silme,
bildirim işlemleri ve güvenlik loglama fonksiyonları.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from models_app.models import UserFavorite, Review, Notification, UserActivity, SecurityLog
from allauth.account.forms import ResetPasswordForm
from django.core.mail import send_mail
from django.conf import settings


def get_client_ip(request):
    """İstemcinin gerçek IP adresini döndürür (proxy desteği dahil)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def login_view(request):
    """
    Kullanıcı giriş view'ı.
    Başarılı/başarısız girişleri SecurityLog'a kaydeder.
    5 başarısız denemede admin'e uyarı maili gönderir.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        ip = get_client_ip(request)
        if user:
            login(request, user)
            # Başarılı girişi logla
            SecurityLog.objects.create(
                ip_address=ip,
                username=username,
                action='login_success',
                success=True
            )
            return redirect('home')
        else:
            # Başarısız girişi logla
            SecurityLog.objects.create(
                ip_address=ip,
                username=username,
                action='login_failed',
                success=False
            )
            # 5 başarısız deneme varsa admin'e uyarı maili gönder
            failed_attempts = SecurityLog.objects.filter(
                ip_address=ip,
                action='login_failed',
                success=False
            ).count()
            if failed_attempts >= 5 and failed_attempts % 5 == 0:
                try:
                    send_mail(
                        subject=f'⚠️ Şüpheli Giriş Denemesi: {ip}',
                        message=f'IP: {ip}\nKullanıcı adı: {username}\nBaşarısız deneme sayısı: {failed_attempts}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=['ozgurhillesiz@outlook.com'],
                        fail_silently=True,
                    )
                except:
                    pass
            return render(request, 'users/login.html', {'error': True})
    return render(request, 'users/login.html')


def logout_view(request):
    """Kullanıcı çıkış işlemi — oturumu kapatır ve ana sayfaya yönlendirir."""
    logout(request)
    return redirect('home')


def custom_password_reset(request):
    """Allauth ResetPasswordForm kullanan özel şifre sıfırlama view'ı."""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            form.save(request)
            return render(request, 'account/password_reset_done.html')
    else:
        form = ResetPasswordForm()
    return render(request, 'account/password_reset.html', {'form': form})


@login_required
def profile_view(request):
    """
    Kullanıcı profil sayfası.
    Favoriler, yorumlar, bildirimler ve aktivite geçmişini gösterir.
    Bio güncelleme işlemlerini yönetir.
    """
    # Kullanıcıya ait verileri select_related ile optimize edilmiş sorgularla çek
    favorites = UserFavorite.objects.filter(user=request.user).select_related('model')
    reviews = Review.objects.filter(user=request.user).select_related('model').order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    activities = UserActivity.objects.filter(user=request.user).select_related('model')[:20]

    if request.method == 'POST':
        # Bio güncelleme
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
def delete_account(request):
    """
    Hesap silme işlemi.
    Silme olayını SecurityLog'a kaydeder, admin'e bildirim maili gönderir,
    oturumu kapatır ve kullanıcıyı siler.
    """
    if request.method == 'POST':
        user = request.user
        username = user.username
        email = user.email
        ip = get_client_ip(request)

        # Hesap silme olayını güvenlik loguna kaydet
        SecurityLog.objects.create(
            ip_address=ip,
            username=username,
            action='account_deleted',
            success=True
        )

        # Admin'e bildirim maili gönder
        try:
            send_mail(
                subject=f'❌ Hesap Silindi: {username}',
                message=f'Bir kullanıcı hesabını sildi.\n\nKullanıcı adı: {username}\nEmail: {email}\nIP: {ip}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ozgurhillesiz@outlook.com'],
                fail_silently=True,
            )
        except:
            pass

        logout(request)
        user.delete()
        messages.success(request, 'Hesabın başarıyla silindi.')
        return redirect('home')
    return redirect('profile')


@login_required
def mark_notification_read(request, pk):
    """Belirtilen bildirimi okundu olarak işaretler."""
    try:
        notif = Notification.objects.get(pk=pk, user=request.user)
        notif.is_read = True
        notif.save()
    except:
        pass
    return redirect('profile')


@login_required
def mark_all_read(request):
    """Kullanıcının tüm okunmamış bildirimlerini toplu okundu yapar."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('profile')


@login_required
def notification_count(request):
    """AJAX için okunmamış bildirim sayısını JSON olarak döndürür."""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})