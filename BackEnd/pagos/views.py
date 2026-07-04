from django.shortcuts import render
from rest_framework.decorators import api_view
from stripe import StripeClient
import stripe
from dotenv import load_dotenv
import os

        
