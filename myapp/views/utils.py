from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from myapp.models import *
from myapp.serializers import *
from myapp import serializers
from django.db.models import Q
from myapp.client import *
from myapp.dao import *
from myapp import forms
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
import myapp.views.permissions as mypermissions
import jwt
import hashlib
from enum import Enum


class ContractAction(Enum):
    CHARGE = 'charge'
    PAY = 'pay'
    ACCEPT = 'accept'
    REJECT = 'reject'
    CONFIRM = 'confirm'
    DENY = 'deny'
    CLAIM = 'claim'
    END = 'end'


LOGIN_ROLES = ['user', 'judge']
SPECIAL_LOGIN_ROLES = ['reporter', 'admin']

KEY = 'secret'
ALGORITHM = 'HS256'

COOKIES_KEYS = [
    'username',
    'role',
    # 'islogin'
]


def generate_token(payload):
    hashed = calculate_hash(payload)
    encoded = jwt.encode({'hashed': hashed}, KEY, algorithm=ALGORITHM).decode("utf-8")
    return encoded


def decode_token(token):
    decoded = jwt.decode(token, KEY, algorithm=ALGORITHM)
    return decoded


def calculate_hash(payload):
    return hashlib.sha256(concat_fields(payload).encode("utf-8")).hexdigest()


def concat_fields(payload):
    result = ""
    for k, v in payload.items():
        result += str(k) + str(v)
    return result


def set_cookies(response, payload):
    for k, v in payload.items():
        response.set_cookie(key=k, value=v, httponly=True)


def get_cookie(request, cookie_key):
    return request.COOKIES.get(cookie_key)


def get_cookies(request, cookies_keys):
    cookies_values = {}
    for k in cookies_keys:
        cookies_values.update({
            k: get_cookie(request, k)
        })
    return cookies_values


def get_date_from_cookies(request):
    return get_cookies(request, COOKIES_KEYS)


def get_token_from_cookies(request):
    return get_cookie(request, 'token')


