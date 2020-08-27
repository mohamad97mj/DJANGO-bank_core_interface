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
        fields = ['bank_account_id', 'owner_type']


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeProfile
        fields = ['national_id', 'name']


class NormalContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalContract
        fields = ['id', 'expire_date', 'settlement_type', 'value_in_rial', 'remittance_currency', 'remittance_value',
                  'judge_name', 'judge_national_id', 'src_owner_bank_account_id', 'dst_owner_bank_account_id', 'status',
                  'description', 'judge_vote']


class SubcontractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcontract
        fields = ['id', 'expire_date', 'value_in_rial', 'remittance_value', 'status', 'description', 'dst_owner',
                  'parent', 'judge_vote']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'otherside_owner', 'value', 'operator_type', 'operator']
