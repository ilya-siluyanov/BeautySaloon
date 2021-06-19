from django import forms
from BeautySaloonApplication.models import Service


class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена', 'class': 'form-control'})
        }
