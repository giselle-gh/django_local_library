import os

import django_heroku
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j142-f%2z1*=8#p%fpg-g53*q4l*-(_kgo9)^^+-8cn39_7i5l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #Solo surante el debug


ALLOWED_HOSTS = ['jobandcar.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'betterforms',
    'appjobcar'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = (
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
)


ROOT_URLCONF = 'pjobcar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pjobcar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobcar',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]
# https://docs.djangoproject.com/en/2.1/topics/i18n/

SITE_ID = 1 

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'#GMT+2

USE_I18N = True

USE_L10N = False

USE_TZ = True
'''
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #Solo surante el debug

    EMAIL_USE_TLS = True

    EMAIL_HOST = 'smtp.gmail.com'

    #EMAIL_PORT = 25

    EMAIL_PORT = 587

    EMAIL_HOST_USER = 'jobandcarspain@gmail.com'

    EMAIL_HOST_PASSWORD = '@Gg04122000'
else:
    EMAIL_BACKEND = (
        'django.core.mail.backends.smtp.EmailBackend'
    )  

'''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jobandcarspain@gmail.com'
EMAIL_HOST_PASSWORD = '@Gg04122000'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#reCAPTCHA
GOOGLE_RECAPTCHA_SECRET_KEY = '6LfHgaMZAAAAAHEj2UkRmoFOf296GRnBWH7uC0AX'

#Donde redirigir si el usuario hace login

LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = '/home/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#Donde subir los documentos
MEDIA_ROOT = os.path.join(BASE_DIR,'static')  

MEDIA_URL = '/media/' 

#Para poder utilizar UserManage en el modelo de usuario
AUTH_USER_MODEL = 'users_management.UserManage'
AUTH_USER_MODEL = 'appjobcar.Usuario'

# Activate Django-Heroku.
django_heroku.settings(locals())
