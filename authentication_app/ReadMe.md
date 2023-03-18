**Install Required dependencies**
1. django-rest-knox 
2. google-api-python-client
3. google-auth

<br/>

**In urls.py append urlpatterns list with:**

`path('auth/', include('authentication_app.urls'))`

<br/>

**In settings.py Add the following things:-**

1. In INSTALLED_APPS list append the 
   1. 'knox'
   2. 'authentication_app'


2. Add:- 
     
    `AUTH_USER_MODEL = 'authentication_app.CustomUser'`


3. Add below dictionaries:-


    REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',)
    }


    REST_KNOX = {
    'USER_SERIALIZER': 'authentication_app.serializers.UserSerializer',
    'TOKEN_TTL': timedelta(hours=24)  # Token Expiry time
    }