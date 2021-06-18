from django import forms

from BeautySaloonApplication.utils import validate_phone_number


class OrderForm(forms.Form):
    phone_number = forms.CharField(max_length=12, min_length=12, validators=[validate_phone_number])
    service_id = forms.CharField(widget=forms.HiddenInput, max_length=100)
    date = forms.CharField(widget=forms.SplitDateTimeWidget(date_format='%d-%m-%Y',
                                                            time_format='%H:%M:%S'),)
