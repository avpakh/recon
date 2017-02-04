"""jas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from datadb import urls as datadb_url
from prognoz import urls as prognoz_url
from maps import urls as maps_url
from gismap import urls as gismap_url
from datadb.views import index_view

from django.conf.urls.static import static

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
               url(r'^$', index_view, name='home'),
               url(r'^datadb/', include(datadb_url)),
               url(r'^maps/', include(maps_url)),
               url(r'^gismap/', include(gismap_url)),
               url(r'^prognoz/', include(prognoz_url)),
                ]


if settings.DEBUG:

    if settings.MEDIA_ROOT:


        urlpatterns += static(settings.MEDIA_URL,

            document_root=settings.MEDIA_ROOT)

    urlpatterns += staticfiles_urlpatterns()

