from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AIModel, Benchmark, PriceHistory, UserFavorite, Review, SubscriptionPlan, Notification, UserActivity
from .serializers import AIModelSerializer, BenchmarkSerializer, PriceHistorySerializer, UserFavoriteSerializer
from .api_service import fetch_huggingface_models, get_model_stats, get_usd_to_try, fetch_ai_news, get_exchange_rates

def home(request):
    models = AIModel.objects.filter(category='model')
    companies = AIModel.objects.filter(category='model').values_list('company', flat=True).distinct()
    
    search = request.GET.get('search', '')
    company = request.GET.get('company', '')
    is_free = request.GET.get('is_free', '')
    is_multimodal = request.GET.get('is_multimodal', '')
    sort = request.GET.get('sort', '')

    if search:
        models = models.filter(Q(name__icontains=search) | Q(company__icontains=search))
    if company:
        models = models.filter(company=company)
    if is_free:
        models = models.filter(is_free=True)
    if is_multimodal:
        models = models.filter(is_multimodal=True)

    if sort == 'price_asc':
        models = models.order_by('input_price')
    elif sort == 'price_desc':
        models = models.order_by('-input_price')
    elif sort == 'rating':
        models = models.annotate(avg_r=Avg('reviews__rating')).order_by('-avg_r')
    elif sort == 'context':
        models = models.order_by('-context_window')
    elif sort == 'newest':
        models = models.order_by('-release_date')
    else:
        models = models.order_by('id')

    paginator = Paginator(models, 6)
    page = request.GET.get('page')
    models = paginator.get_page(page)

    rates = cache.get('exchange_rates')
    if not rates:
        rates = get_exchange_rates()
        cache.set('exchange_rates', rates, 60 * 30)

    top_rated = AIModel.objects.filter(category='model').annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).filter(num_reviews__gt=0).order_by('-avg_rating')[:5]

    most_favorited = AIModel.objects.filter(category='model').annotate(
        fav_count=Count('userfavorite')
    ).order_by('-fav_count')[:5]

    total_reviews = Review.objects.count()

    return render(request, 'models_app/home.html', {
        'models': models,
        'companies': companies,
        'search': search,
        'usd_to_try': rates['TRY'],
        'top_rated': top_rated,
        'most_favorited': most_favorited,
        'total_reviews': total_reviews,
    })

def tools(request):
    tools = AIModel.objects.filter(category='tool').order_by('name')
    search = request.GET.get('search', '')
    is_free = request.GET.get('is_free', '')

    if search:
        tools = tools.filter(Q(name__icontains=search) | Q(company__icontains=search))
    if is_free:
        tools = tools.filter(is_free=True)

    return render(request, 'models_app/tools.html', {
        'tools': tools,
        'search': search,
    })

def model_detail(request, pk):
    ai_model = get_object_or_404(AIModel, pk=pk)
    benchmarks = ai_model.benchmarks.all()
    price_history = ai_model.price_history.all().order_by('date')
    reviews = ai_model.reviews.all().order_by('-created_at')
    plans = ai_model.plans.all().order_by('price')
    users = User.objects.exclude(pk=request.user.pk) if request.user.is_authenticated else []
    user_review = None
    is_favorite = False
    usd_to_try = cache.get('usd_to_try') or get_usd_to_try()
    if request.user.is_authenticated:
        is_favorite = UserFavorite.objects.filter(user=request.user, model=ai_model).exists()
        user_review = Review.objects.filter(user=request.user, model=ai_model).first()
    return render(request, 'models_app/detail.html', {
        'ai_model': ai_model,
        'benchmarks': benchmarks,
        'price_history': price_history,
        'reviews': reviews,
        'plans': plans,
        'users': users,
        'user_review': user_review,
        'is_favorite': is_favorite,
        'usd_to_try': usd_to_try,
    })

@login_required
def recommend_model(request, pk):
    ai_model = get_object_or_404(AIModel, pk=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            target_user = User.objects.get(username=username)
            if target_user == request.user:
                messages.error(request, 'Kendine öneri gönderemezsin!')
            else:
                Notification.objects.create(
                    user=target_user,
                    message=f'🤖 {request.user.username} sana "{ai_model.name}" modelini önerdi!',
                    link=f'/model/{pk}/'
                )
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='recommend',
                    model=ai_model,
                    description=f'"{ai_model.name}" modelini {target_user.username} kullanıcısına önerdi.'
                )
                messages.success(request, f'{target_user.username} kullanıcısına öneri gönderildi!')
        except User.DoesNotExist:
            messages.error(request, 'Kullanıcı bulunamadı!')
    return redirect('model_detail', pk=pk)

@login_required
def add_review(request, pk):
    ai_model = get_object_or_404(AIModel, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                user=request.user,
                model=ai_model,
                defaults={'rating': rating, 'comment': comment}
            )
            Notification.objects.create(
                user=request.user,
                message=f'"{ai_model.name}" modeline {rating} yıldız verdin.',
                link=f'/model/{pk}/'
            )
            UserActivity.objects.create(
                user=request.user,
                activity_type='review',
                model=ai_model,
                description=f'"{ai_model.name}" modeline {rating} yıldız verdi.'
            )
            messages.success(request, 'Yorumun eklendi!')
        return redirect('model_detail', pk=pk)
    return redirect('model_detail', pk=pk)

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    model_pk = review.model.pk
    review.delete()
    messages.success(request, 'Yorumun silindi!')
    return redirect('model_detail', pk=model_pk)

def compare(request):
    selected_ids = request.GET.getlist('models')
    selected_models = AIModel.objects.filter(id__in=selected_ids).prefetch_related('plans')
    all_models = AIModel.objects.filter(category='model')

    if request.user.is_authenticated and selected_models:
        for m in selected_models:
            UserActivity.objects.create(
                user=request.user,
                activity_type='compare',
                model=m,
                description=f'"{m.name}" modelini karşılaştırdı.'
            )

    return render(request, 'models_app/compare.html', {
        'selected_models': selected_models,
        'all_models': all_models,
    })

@login_required
def toggle_favorite(request, pk):
    ai_model = get_object_or_404(AIModel, pk=pk)
    fav, created = UserFavorite.objects.get_or_create(user=request.user, model=ai_model)
    if not created:
        fav.delete()
        Notification.objects.create(
            user=request.user,
            message=f'"{ai_model.name}" favorilerinden çıkarıldı.',
            link=f'/model/{pk}/'
        )
        UserActivity.objects.create(
            user=request.user,
            activity_type='unfavorite',
            model=ai_model,
            description=f'"{ai_model.name}" modelini favorilerden çıkardı.'
        )
    else:
        Notification.objects.create(
            user=request.user,
            message=f'"{ai_model.name}" favorilere eklendi! ❤️',
            link=f'/model/{pk}/'
        )
        UserActivity.objects.create(
            user=request.user,
            activity_type='favorite',
            model=ai_model,
            description=f'"{ai_model.name}" modelini favorilere ekledi.'
        )
    return redirect('model_detail', pk=pk)

@login_required
def favorites(request):
    favs = UserFavorite.objects.filter(user=request.user).select_related('model')
    return render(request, 'models_app/favorites.html', {'favs': favs})

def trending(request):
    hf_models = cache.get('hf_trending')
    if not hf_models:
        hf_models = fetch_huggingface_models(limit=12)
        cache.set('hf_trending', hf_models, 60 * 10)
    return render(request, 'models_app/trending.html', {
        'hf_models': hf_models,
    })

def model_hf_detail(request, model_id):
    cache_key = f'hf_model_{model_id}'
    hf_model = cache.get(cache_key)
    if not hf_model:
        hf_model = get_model_stats(model_id)
        cache.set(cache_key, hf_model, 60 * 10)
    return render(request, 'models_app/hf_detail.html', {
        'hf_model': hf_model,
    })

def news(request):
    articles = cache.get('ai_news')
    if not articles:
        articles = fetch_ai_news(settings.NEWS_API_KEY)
        cache.set('ai_news', articles, 60 * 30)
    return render(request, 'models_app/news.html', {
        'articles': articles,
    })

def recommend(request):
    use_case = request.GET.get('use_case', '')
    budget = request.GET.get('budget', '')
    need_multimodal = request.GET.get('need_multimodal', '')
    recommended = []

    if use_case or budget or need_multimodal:
        models = AIModel.objects.filter(category='model')

        if need_multimodal == 'yes':
            models = models.filter(is_multimodal=True)

        if budget == 'free':
            models = models.filter(is_free=True)
        elif budget == 'low':
            models = models.filter(input_price__lte=0.000003)
        elif budget == 'high':
            models = models.filter(input_price__gte=0.000003)

        if use_case == 'coding':
            models = models.filter(Q(name__icontains='gpt') | Q(name__icontains='claude') | Q(name__icontains='deepseek'))
        elif use_case == 'writing':
            models = models.filter(Q(name__icontains='claude') | Q(name__icontains='gpt'))
        elif use_case == 'image':
            models = models.filter(is_multimodal=True)
        elif use_case == 'research':
            models = models.filter(Q(name__icontains='perplexity') | Q(name__icontains='gpt') | Q(name__icontains='gemini'))
        elif use_case == 'math':
            models = models.filter(Q(name__icontains='deepseek') | Q(name__icontains='gpt') | Q(name__icontains='claude'))

        recommended = models[:4]

    return render(request, 'models_app/recommend.html', {
        'recommended': recommended,
        'use_case': use_case,
        'budget': budget,
        'need_multimodal': need_multimodal,
    })

def stats(request):
    total_models = AIModel.objects.filter(category='model').count()
    total_tools = AIModel.objects.filter(category='tool').count()
    total_reviews = Review.objects.count()
    total_users = User.objects.count()
    total_favorites = UserFavorite.objects.count()
    top_models = AIModel.objects.filter(category='model').annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).filter(num_reviews__gt=0).order_by('-avg_rating')[:10]
    most_favorited = AIModel.objects.annotate(
        fav_count=Count('userfavorite')
    ).order_by('-fav_count')[:10]
    return render(request, 'models_app/stats.html', {
        'total_models': total_models,
        'total_tools': total_tools,
        'total_reviews': total_reviews,
        'total_users': total_users,
        'total_favorites': total_favorites,
        'top_models': top_models,
        'most_favorited': most_favorited,
    })

class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q', '')
        models = AIModel.objects.filter(Q(name__icontains=q) | Q(company__icontains=q))
        serializer = self.get_serializer(models, many=True)
        return Response(serializer.data)

class BenchmarkViewSet(viewsets.ModelViewSet):
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]