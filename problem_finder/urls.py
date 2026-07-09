from django.urls import path, include
from django.conf import settings
from django.shortcuts import render
from analytics.admin_site import custom_admin_site

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

admin_urlconf = custom_admin_site.urls

urlpatterns = [
    path('', include('core.urls')),
    path('', include('survey.urls')),
    path(settings.ADMIN_URL, include((admin_urlconf[0], admin_urlconf[1]), namespace=admin_urlconf[2])),
    path('export/', include('analytics.urls')),
]

handler404 = page_not_found
