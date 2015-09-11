from django import forms
from django.forms.widgets import DateInput
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class CustomReport(forms.Form):
    startDate = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type':'date', 'class':'form-control',}))
    startTime = forms.TimeField(label='Start Time', widget=forms.TimeInput(attrs={'type':'time', 'class':'form-control',}))
    
    endDate = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type':'date', 'class':'form-control',}))
    endTime = forms.TimeField(label='End Time', widget=forms.TimeInput(attrs={'type':'time', 'class':'form-control',}))
    
    tzOffset = forms.CharField(widget=forms.HiddenInput(attrs={'value':'', 'class':'hidden-tz'}))
    