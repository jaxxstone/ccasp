'''This module contains the fields and information used to generate a custom
report form for the user. '''
# pylint: disable=no-value-for-parameter, unexpected-keyword-arg

from django import forms
from django.forms.widgets import DateInput
from functools import partial
import pytz

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class CustomReport(forms.Form):
    '''Form object for generating custom sensor report'''
    startDate = forms.DateField(
        label='Start Date', widget=forms.DateInput(
            attrs={'type':'date', 'class':'form-control',}))
    startTime = forms.TimeField(
        label='Start Time', widget=forms.TimeInput(
            attrs={'type':'time', 'class':'form-control',}))

    endDate = forms.DateField(
        label='End Date', widget=forms.DateInput(
            attrs={'type':'date', 'class':'form-control',}))
    endTime = forms.TimeField(
        label='End Time', widget=forms.TimeInput(
            attrs={'type':'time', 'class':'form-control',}))

    tzOffset = forms.CharField(
        widget=forms.HiddenInput(attrs={'value':'', 'class':'hidden-tz'}))

class EditProfileForm(forms.Form):
    tz_choices = zip(pytz.common_timezones, pytz.common_timezones)
    timezone = forms.ChoiceField(label='Timezone',
                                 choices=(tz_choices))

    notifications = forms.BooleanField(label='Receive E-mail Notifications')
