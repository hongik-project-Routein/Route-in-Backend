import googlemaps
import json
from django.conf import settings
from django.shortcuts import render, redirect
import secretKeys

def geocode(request):
    GOOGLE_API_KEY = secretKeys.GOOGLE_API_KEY
    GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

