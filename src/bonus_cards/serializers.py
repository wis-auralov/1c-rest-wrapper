from rest_framework import serializers
from bonus_cards.models import BonusCard


class BonusCardBaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        return BonusCard(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance


class BonusCardGetUuidSerializer(BonusCardBaseSerializer):
    uuid = serializers.UUIDField()


class BonusCardBalanceSerializer(BonusCardBaseSerializer):
    uuid = serializers.UUIDField()
    balance = serializers.IntegerField()


class BonusCardTransactionsSerializer(BonusCardBaseSerializer):
    uuid = serializers.UUIDField()
    transactions = serializers.ListField(child=serializers.DictField())
