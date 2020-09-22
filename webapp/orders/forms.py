from django import forms
from django.forms import ModelForm
from .models import Order


class OrderCreateForm(ModelForm):
