from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-kk#g9_n103(x+ss)i64k6g3f6#uj-u+iwfh%b2nqv)bedk_rxq')
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'models_app',
    'users',
    'csp',
]

MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'models_app.context_processors.admin_stats',
           ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'modularena-cache',
    }
}

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Render'da PostgreSQL kullan (DATABASE_URL varsa)
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'models_app.validators.CustomPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
ACCOUNT_PASSWORD_RESET_REDIRECT_URL = '/accounts/password/reset/done/'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[ModelArena] '

# Güvenlik ayarları
if os.environ.get('RENDER'):
    DEBUG = False
    ALLOWED_HOSTS = ['.onrender.com']
    CSRF_TRUSTED_ORIGINS = ['https://modelarena-t331.onrender.com']

    # HTTPS güvenliği
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Cookie güvenliği
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True

# Güvenlik header'ları
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# Session güvenliği
SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# Brute force koruması
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m',
}

# Content Security Policy
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'style-src': ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net",),
        'script-src': ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net",),
        'img-src': ("'self'", "data:", "https:", "http:",),
        'font-src': ("'self'", "https://cdn.jsdelivr.net",),
    }
}

# Email — Render'da Brevo API (port sorunu yok), lokalde konsola yaz
BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')

if BREVO_API_KEY:
    EMAIL_BACKEND = 'users.email_backend.BrevoAPIBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'ModelArena <ozgurhillesiz@outlook.com>'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

NEWS_API_KEY = '711544257dc944e299e23fdc235a9797'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dombsidxn',
    'API_KEY': '981613112275284',
    'API_SECRET': 'w_hputSrwqvGKZwxwHQJ2msolGM',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ===== Jazzmin Admin Teması =====
JAZZMIN_SETTINGS = {
    "site_title": "ModelArena Yönetim",
    "site_header": "ModelArena",
    "site_brand": "ModelArena",
    "site_logo": "img/logo.svg",
    "login_logo": "img/logo.svg",
    "site_icon": "img/favicon.ico",
    "welcome_sign": "ModelArena Yönetim Paneline Hoş Geldiniz",
    "copyright": "ModelArena",
    "search_model": ["models_app.AIModel", "auth.User"],

    # Üst menü
    "topmenu_links": [
        {"name": "Siteye Git", "url": "/", "new_window": True},
        {"name": "Modeller", "model": "models_app.AIModel"},
        {"name": "Kullanıcılar", "model": "auth.User"},
    ],

    # Sol menü ikonları
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "models_app.AIModel": "fas fa-robot",
        "models_app.Review": "fas fa-star",
        "models_app.UserFavorite": "fas fa-heart",
        "models_app.ReviewLike": "fas fa-thumbs-up",
        "models_app.SubscriptionPlan": "fas fa-credit-card",
        "models_app.Benchmark": "fas fa-trophy",
        "models_app.PriceHistory": "fas fa-chart-line",
        "models_app.Notification": "fas fa-bell",
        "models_app.UserActivity": "fas fa-history",
        "models_app.UserProfile": "fas fa-id-card",
        "models_app.SecurityLog": "fas fa-shield-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,
    "custom_css": "css/admin.css",
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-purple",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-purple",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}