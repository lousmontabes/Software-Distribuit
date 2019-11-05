# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Restaurant, Review, Reservation

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Reservation)
