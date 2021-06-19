from django import forms
from django.forms import TextInput

from BeautySaloonApplication.utils import validate_phone_number


class OrderForm(forms.Form):
    phone_number = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control phone_number_field'}),
                                   max_length=12, min_length=12,
                                   validators=[validate_phone_number])
    service_id = forms.CharField(widget=forms.HiddenInput(),
                                 max_length=100)
    date = forms.CharField(widget=forms.DateInput(
        attrs={'type': 'date',
               'class': 'form-control',
               'placeholder': 'Введите дату'},
        format='%d:%m:%Y'))
    time = forms.CharField(widget=forms.TimeInput(
        attrs={'type': 'time',
               'class': 'form-control',
               'placeholder': 'Введите время'},
        format='%H:%M'
    ))
