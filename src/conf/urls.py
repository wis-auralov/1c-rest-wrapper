from django.conf.urls import patterns, include, url
from django.contrib import admin

from customers.urls import router


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    url(r'^customers/', include(router.urls)),
    url(r'^bonus_cards/',
        include("bonus_cards.urls", namespace='bonus_cards')),
)
