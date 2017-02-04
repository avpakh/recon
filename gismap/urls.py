from django.conf.urls import url, include
from gismap.views import map_page


urlpatterns = [

 url(r'^map/',map_page,name='map_page'),
]