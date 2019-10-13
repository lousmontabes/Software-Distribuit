# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
import json

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def index(request):
    context = {}
    return render(request, 'index.html', context)

def airports(request):
    with open('vueling/static/airports.json', 'r') as fp:
        airports = json.load(fp)

    return JsonResponse(airports)