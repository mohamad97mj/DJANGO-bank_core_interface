from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from myapp import models
from myapp import forms
from myapp import serializers
from django.db.models import Q


def get_user(pk):
    try:
        return models.UserProfile.objects.get(pk=pk)
    except models.UserProfile.DoesNotExist:
        raise Http404


def get_judge(pk):
    try:
        return models.JudgeProfile.objects.get(pk=pk)
    except models.JudgeProfile.DoesNotExist:
        raise Http404


def get_owner(pk):
    try:
        return models.Owner.objects.get(pk=pk)
    except models.Owner.DoesNotExist:
        raise Http404


def get_contract(pk):
    try:
        return models.Contract.objects.get(pk=pk)
    except models.Contract.DoesNotExist:
        raise Http404


def get_subcontract(pk):
    try:
        return models.Subcontract.objects.get(pk=pk)
    except models.Subcontract.DoesNotExist:
        raise Http404


def get_transaction(pk):
    try:
        return models.Transaction.objects.get(pk=pk)
    except models.Transaction.DoesNotExist:
        raise Http404
