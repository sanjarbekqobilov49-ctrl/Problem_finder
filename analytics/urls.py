from django.urls import path
from . import views

urlpatterns = [
    path('csv/', views.export_csv, name='export_csv'),
    path('excel/', views.export_excel, name='export_excel'),
]
