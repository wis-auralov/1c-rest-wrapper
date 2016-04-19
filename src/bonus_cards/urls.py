from django.conf.urls import patterns, url
from bonus_cards.views import (
    api_root, BonusCardBalanceView, BonusCardTransactionsView,
    BonusCardGetUuidView,
)

urlpatterns = patterns(
    'bonus_cards.views',
    url('^$', api_root),
    url(
        r'^get_uuid/(?P<bonus_program_uuid>[\w-]+)/(?P<card_number>\w+)/$',
        BonusCardGetUuidView.as_view(), name='get_uuid'
    ),
    url(
        r'^balance/(?P<uuid>[\w-]+)/$', BonusCardBalanceView.as_view(),
        name='balance'
    ),
    url(
        r'^transactions/(?P<uuid>[\w-]+)/$',
        BonusCardTransactionsView.as_view(), name='transactions'
    ),
)
