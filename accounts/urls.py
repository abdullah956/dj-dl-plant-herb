from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history, name='history'),
    path('history/delete/', views.delete_history, name='delete_history'),
path('history/delete/<int:record_id>/', views.delete_single_history, name='delete_single_history'),
]
