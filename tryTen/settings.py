"""
Django settings for tryTen project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_SECRET_KEY", "pk_YOUR_TEST_PUBLIC_KEY")
# STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "pk_YOUR_TEST_SECRET_KEY")

STRIPE_PUBLISHABLE_KEY = 'pk_test_ntsnlkXckptVryVtY7Sty15Z'

STRIPE_SECRET_KEY = 'sk_test_numkG8DOp8a20m0001zkZTH8'


EASYPOST_TEST_KEY = "kDBRViD7fuwv11a9miyn0w"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aleclivinghouse@gmail.com'
EMAIL_HOST_PASSWORD = 'Voodoo12'
EMAIL_PORT = '587'
#this is the port for gmail
EMAIL_USE_TLS = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ktaws9ushmnohnnom!mnzf6m@=z#%fr-68o6n1kwm!m9qhyzna'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles',
    'contact',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'checkout',
    'stripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tryTen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)


WSGI_APPLICATION = 'tryTen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]



STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

SITE_ID = 1

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL =  '/'

ACCOUNT_AUTHENTIFICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_EMAIL_SUBJECT_PREFIX = "My subject: "
ACCOUNT_DETAIL_HTTP_PROTOCOL = "http"

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_USERNAME_RREQUIRED = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_PASSWORD_MIN_LENGTH = 6
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

#if I want to change the fields in the signup form:
# class SignupForm(forms.Form):
#     first_name = forms.CharField(max_length=30, label='Voornaam')
#     last_name = forms.CharField(max_length=30, label='Achternaam')
#
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
# Then, in your settings point to this form:
#
# ACCOUNT_SIGNUP_FORM_CLASS = 'yourproject.yourapp.forms.SignupForm'
