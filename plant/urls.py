from django.urls import path
from .views import home_view, predict_view ,contact_view,subscribe_newsletter


urlpatterns = [
    path("predict/", predict_view, name="predict"),
    path("", home_view, name="home"),
    path('contact/', contact_view, name='contact'),
    path("subscribe/", subscribe_newsletter, name="subscribe"),
]
