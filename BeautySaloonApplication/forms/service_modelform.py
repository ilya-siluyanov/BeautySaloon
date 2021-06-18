from django import forms
from BeautySaloonApplication.models import Service


class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
