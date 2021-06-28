from django import forms
from django.db import models
from django.db.models import fields

from BeautySaloonApplication.utils import validate_phone_number


class Client(models.Model):
    phone_number = fields.CharField(primary_key=True, max_length=12)
    name = fields.CharField(max_length=50)


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = fields.CharField(max_length=255)
    price = fields.IntegerField(default=0)


class Order(models.Model):
    order_id = fields.AutoField(primary_key=True)
    client = models.ForeignKey(related_name='orders', to=Client, on_delete=models.CASCADE)
    service = models.ForeignKey(related_name='orders', to=Service, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, default='2000-01-01')
    time = models.TimeField(null=False, blank=False, default='00:00')
    is_complete = fields.BooleanField(default=False)


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


class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        # форма содержит все поля описанной ранее модели Service
        # поле service_id будет скрытым полем формы
        fields = '__all__'
        # опишем, как будут выглядеть поля формы в HTML-коде
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена', 'class': 'form-control'})
        }
