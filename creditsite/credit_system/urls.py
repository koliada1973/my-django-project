from django.urls import path

from credit_system.views import *

urlpatterns = [
    path('', index, name='index'),
    path('credits/<int:credid>/', credits_list, name='credits'),

]

