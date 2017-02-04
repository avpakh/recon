from django.conf.urls import url, include
from datadb.views import map_page,table_page,update_page,graph_page,request_page,list_status, showdetail,showtypes,graphs_page


urlpatterns = [
    url(r'^$', list_status,name='get_data'),
    url(r'^map/',map_page,name='map_page'),
    url(r'^tables/',table_page),
    url(r'^update/',update_page),
    url(r'^graphs/',graph_page),
    url(r'^request/',request_page),
    url(r'^(?P<pk>[0-9]+)/$', showdetail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', showtypes, name='analys'),
    url(r'^graph/(?P<pk>[0-9]+)/$', graphs_page, name='graphs'),

]
