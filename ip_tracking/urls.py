from django.urls import path
from ip_tracking.views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
]

