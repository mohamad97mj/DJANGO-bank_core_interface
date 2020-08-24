from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from myapp.models import *
from myapp.serializers import *
from myapp import serializers
from django.db.models import Q
import requests


def get_user(pk):
    try:
        return UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        raise Http404


def get_judge(pk):
    try:
        return JudgeProfile.objects.get(pk=pk)
    except JudgeProfile.DoesNotExist:
        raise Http404


def get_owner(pk):
    try:
        return Owner.objects.get(pk=pk)
    except Owner.DoesNotExist:
        raise Http404


def get_contract(pk):
    try:
        return NormalContract.objects.get(pk=pk)
    except NormalContract.DoesNotExist:
        raise Http404


def get_subcontract(pk):
    try:
        return Subcontract.objects.get(pk=pk)
    except Subcontract.DoesNotExist:
        raise Http404


def get_transaction(pk):
    try:
        return Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        raise Http404
