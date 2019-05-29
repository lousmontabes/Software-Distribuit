# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Restaurant, ViewedRestaurants, RestaurantInsertDate, Review
from .forms import ReservationForm, PickerForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib import auth

def index(request):
    promoted_restaurants =  Restaurant.objects.filter()
    categories = Restaurant._d_categories
    viewedrestaurants = _check_session(request)

    if request.method == "POST":
        form = PickerForm(request.POST)
        if form.is_valid():
                data = form.cleaned_data

        return HttpResponseRedirect(reverse('restaurants', args=[data['city'], data['category']]))

    context = {
        'restaurants': promoted_restaurants,
        'viewedrestaurants': viewedrestaurants,
        'form': PickerForm(label_suffix='', initial={'category': 'Medi', 'city': 'barcelona'})
    }

    return render(request, 'forkilla/index.html', context)

def restaurants(request, city="", category=""):

    promoted = False
    human_category = None

    categories = Restaurant._d_categories
    viewedrestaurants = _check_session(request)

    try:
        human_category = categories[category.capitalize()]
    except KeyError:
        pass

    if city and human_category:
        restaurants_by_city = Restaurant.objects.filter(city__iexact=city, category__iexact=category)

    else:
        if city:
            restaurants_by_city = Restaurant.objects.filter(city__iexact=city)
        else:
            restaurants_by_city =  Restaurant.objects.filter(is_promot="True")
            promoted = True

    if request.method == "POST":
        form = PickerForm(request.POST)
        if form.is_valid():
                data = form.cleaned_data

        return HttpResponseRedirect(reverse('restaurants', args=[data['city'], data['category']]))

    context = {
    	'city': city.capitalize(),
        'category': human_category,
        'restaurants': restaurants_by_city,
        'promoted': promoted,
        'viewedrestaurants': viewedrestaurants,
        'form': PickerForm(label_suffix='', initial={'category': 'Medi', 'city': 'barcelona'})
    }

    return render(request, 'forkilla/restaurants.html', context)

def restaurant(request, restaurant_number=""):

    viewedrestaurants = _check_session(request)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
                review.save()
                request.session["review"] = review.id
                request.session["result"] = "OK"
        else:
              request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('restaurant', args=[restaurant_number]))

    elif request.method == "GET":
        try:
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            lastviewed = RestaurantInsertDate(viewedrestaurants=viewedrestaurants, restaurant=restaurant)

            lastviewed.save()
        except Restaurant.DoesNotExist:
            return render(request, 'forkilla/404.html')

        categories = Restaurant._d_categories

        reviews = []
        try:
            reviews = Review.objects.filter(restaurant=restaurant)
        except Review.DoesNotExist:
            reviews = []

        context = {
            'form': ReviewForm(),
        	'restaurant': restaurant,
            'reviews': reviews,
            'viewedrestaurants': viewedrestaurants
        }

    return render(request, 'forkilla/details.html', context)

def reservation(request):

    viewedrestaurants = _check_session(request)
    categories = Restaurant._d_categories

    try:
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                    resv = form.save(commit=False)
                    restaurant_number = request.session["reserved_restaurant"]
                    resv.restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
                    resv.save()
                    request.session["reservation"] = resv.id
                    request.session["result"] = "OK"

            else:
                  request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkout'))

        elif request.method == "GET":
            restaurant_number = request.GET["reservation"]
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reserved_restaurant"] = restaurant_number

            form = ReservationForm()

            context = {
                'restaurant': restaurant,
                'viewedrestaurants': viewedrestaurants,
                'form': form
            }

    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exist")

    return render(request, 'forkilla/reservation.html', context)

def checkout(request):

    viewedrestaurants = _check_session(request)

    context = {
        'reservation': request.session["reservation"],
        'restaurant': restaurant,
        'viewedrestaurants': viewedrestaurants,
    }

    return render(request, 'forkilla/checkout.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=new_user.username, password=raw_password)
            auth.login(request, user)

            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'forkilla/register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('index'))
            else:
                # Show an error page
                return 0
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'forkilla/login.html', context)

def _login(request, user):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return 1
        #return HttpResponse que toque =D.
    else:
        # Show an error page
        return 0
        #return la httpresponse que toque =(.

def logout(request):
    auth.logout(request)
    return 1
    # Redirect to a success page.
    #return HttpResponse que toque =).

def _check_session(request):

    if "viewedrestaurants" not in request.session:
        viewedrestaurants = ViewedRestaurants()
        viewedrestaurants.save()
        request.session["viewedrestaurants"] = viewedrestaurants.id_vr
    else:
        viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])

    return viewedrestaurants
