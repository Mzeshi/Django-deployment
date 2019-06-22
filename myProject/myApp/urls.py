from myApp import views
from django.urls import path

# TEMPLATE TAG
app_name = 'jmc'

urlpatterns = [
    path('registration/',views.registration,name='registration'),
    path('user_login/',views.user_login,name='user_login'),
]