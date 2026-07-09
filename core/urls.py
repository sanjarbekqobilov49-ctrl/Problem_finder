from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('consent/', views.consent, name='consent'),
    path('start/', views.start_survey, name='start_survey'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
