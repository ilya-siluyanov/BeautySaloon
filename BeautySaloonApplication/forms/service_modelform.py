from django import forms
from BeautySaloonApplication.models import Service


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
