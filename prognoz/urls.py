from django.conf.urls import url, include
from prognoz.views import main,setmap_page,results,post_form_upload



urlpatterns = [
    url(r'^$', main,name='prognoz'),
    url(r'^setmap/',setmap_page,name='setmap_page'),
    url(r'^results/$',results,name='results'),
    url(r'^calc.html$',post_form_upload,name='post_form_upload'),

]
