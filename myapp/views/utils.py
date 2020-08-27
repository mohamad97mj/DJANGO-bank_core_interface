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
from myapp.client import *

