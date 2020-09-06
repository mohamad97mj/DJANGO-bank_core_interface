from abc import ABC

from rest_framework import serializers
from .models import *


class AuthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthProfile
        fields = ['id', 'email', 'full_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        user = model.AuthProfile.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user

    # def update


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['national_code', 'first_name', 'last_name']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['bank_account_id', 'type']


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeProfile
        fields = ['national_id', 'name']


class NormalContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalContract
        fields = [
            'id',
            'src_owner_bank_account_id',
            'dst_owner_bank_account_id',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge_name',
            'judge_national_id',
            # 'judge_vote',
            'expire_date',
            'status',
            'description',
        ]


class SubcontractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcontract
        fields = [
            'id',
            'parent_id',
            'dst_owner',
            'value_in_rial',
            'remittance_value',
            'status',
            'expire_date',
            'judge_vote',
            'description',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'otherside_owner',
            'transaction_type',
            'value',
            'operator_type',
            'operator'
        ]
