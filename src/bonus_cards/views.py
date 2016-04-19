import logging

from suds.client import Client, WebFault

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings

from bonus_cards.models import BonusCard
from bonus_cards.serializers import (
    BonusCardBalanceSerializer, BonusCardTransactionsSerializer,
    BonusCardGetUuidSerializer,
)

LOGGER = logging.getLogger(__name__)

if settings.DEBUG:
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)
    logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
    logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)


@api_view(('GET',))
def api_root(request):
    return Response({
        'get_uuid': reverse(
            'bonus_cards:get_uuid', kwargs={
                'bonus_program_uuid': 'BONUS_PROGRAM_UUID',
                'card_number': 'CARD_NUMBER'
            }
        ),
        'balance': reverse(
            'bonus_cards:balance', kwargs={'uuid': 'CARD_UUID'}
        ),
        'transactions': reverse(
            'bonus_cards:transactions', kwargs={'uuid': 'CARD_UUID'}
        ),
    })


class BonusCardBaseView(generics.RetrieveAPIView):
    def get_wsdl_service(self, wsdl_client):
        raise NotImplementedError

    def get_serialized_data(self, wsdl_data):
        raise NotImplementedError

    def get_object(self):
        try:
            wsdl_client = Client(settings.ONE_C_WSDL,
                                 username=settings.ONE_C_WSDL_USER,
                                 password=settings.ONE_C_WSDL_PASSWORD)

            wsdl_response = self.get_wsdl_service(wsdl_client)

        except (WebFault, Exception) as e:
            LOGGER.error(e)
            wsdl_response = None

        return wsdl_response

    def retrieve(self, request, *args, **kwargs):
        wsdl_obj = self.get_object()
        if wsdl_obj:
            if u'Данные' in wsdl_obj:
                serialized_data = self.get_serialized_data(wsdl_obj[u'Данные'])
                # cache.set(request.path, serialized_data, 60)
                return Response(serialized_data)

            elif u'_Сообщение' in wsdl_obj:
                message = {'message': wsdl_obj[u'_Сообщение']}
                return Response(message, status.HTTP_404_NOT_FOUND)

        else:
            message = {'message': '1C error communication'}
            return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BonusCardGetUuidView(BonusCardBaseView):
    serializer_class = BonusCardGetUuidSerializer

    def get_wsdl_service(self, wsdl_client):
        return wsdl_client.service.BonusCardGetID(
            self.kwargs.get('bonus_program_uuid'),
            self.kwargs.get('card_number'),
        )

    def get_serialized_data(self, wsdl_data):
        bonus_card = BonusCard(uuid=wsdl_data[u'Идентификатор'])
        serializer = self.get_serializer(bonus_card)
        return serializer.data


class BonusCardBalanceView(BonusCardBaseView):
    serializer_class = BonusCardBalanceSerializer

    def get_wsdl_service(self, wsdl_client):
        return wsdl_client.service.BonusCardInfo(self.kwargs.get('uuid'))

    def get_serialized_data(self, wsdl_data):
        balance = wsdl_data[u'Баллы']
        bonus_card = BonusCard(uuid=self.kwargs.get('uuid'), balance=balance)
        serializer = self.get_serializer(bonus_card)
        return serializer.data


class BonusCardTransactionsView(BonusCardBaseView):
    serializer_class = BonusCardTransactionsSerializer

    def get_wsdl_service(self, wsdl_client):
        return wsdl_client.service.BonusCardTransactions(
            self.kwargs.get('uuid')
        )

    def get_serialized_data(self, wsdl_data):
        transactions = []
        for transaction in wsdl_data[u'ИсторияОпераций']:
            transactions.append({
                'period': transaction[u'Период'],
                'balance': transaction[u'Баллы'],
                'comment': transaction[u'Комментарий'],
            })

        bonus_card = BonusCard(uuid=self.kwargs.get('uuid'),
                               transactions=transactions)
        serializer = self.get_serializer(bonus_card)
        return serializer.data
