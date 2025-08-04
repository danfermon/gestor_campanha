## arquivo preparado para produçãp no gcp - o anterior renomei para setting_dev.py ## - Danatielly - 02/08/2025
from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Carrega variáveis do .env
load_dotenv()

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-insegura")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "34.95.220.242",  # IP da sua VM
]

CSRF_TRUSTED_ORIGINS = [
    "http://34.95.220.242",
    "https://34.95.220.242",
]

# teste 
DOMAIN_NAME = os.getenv('DOMAIN_NAME')
if DOMAIN_NAME:
    ALLOWED_HOSTS.append(DOMAIN_NAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{DOMAIN_NAME}")



# Variável para APIs
API_KEY_SEFAZ = os.getenv("API_KEY_SEFAZ")

# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # apps do projeto
    "usuarios",
    "participantes",
    "cupons",
    "skus_validos",

    # libs externas
    "rest_framework",
    "rest_framework.authtoken",
    "widget_tweaks",
    "django_celery_beat",
]

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static sem nginx em dev
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gestor_campanha.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # se tiver templates fora dos apps
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gestor_campanha.wsgi.application"

# Banco de dados
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(os.getenv("DATABASE_URL"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Celery (com Redis)
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JS, etc)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # arquivos durante desenvolvimento
STATIC_ROOT = BASE_DIR / "staticfiles"   # pasta onde o collectstatic coloca tudo
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Arquivos de mídia (imagens, uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Usuário customizado
AUTH_USER_MODEL = "usuarios.Usuarios"

# Login
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "sistema"
LOGOUT_REDIRECT_URL = "login"

# Sessão
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hora

# Datas
DATE_FORMAT = "d/m/Y"
DATE_INPUT_FORMATS = ["%d/%m/%Y"]

# Auto field padrão
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# autenticação para uso da API interna
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

