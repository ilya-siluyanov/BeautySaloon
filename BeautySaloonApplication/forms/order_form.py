from django import forms


class OrderForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    service_id = forms.CharField(widget=forms.HiddenInput, max_length=100)
    date = forms.CharField(widget=forms.SplitDateTimeWidget(date_format='%d-%m-%Y',
                                                            time_format='%H:%M:%S'),
                           )
