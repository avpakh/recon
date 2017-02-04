from django.conf.urls import url, include
from maps.views import main



urlpatterns = [
    url(r'^$', main,name='maps'),
 ]
