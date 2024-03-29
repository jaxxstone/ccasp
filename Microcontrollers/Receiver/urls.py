'''This module contains the URL dispatcher for the Receiver application in 
the 'records' namespace'''

from django.conf.urls import url
from Receiver.views import admin, dashboard, overview, daily_report,\
    weekly_report, monthly_report, yearly_report, custom_form, \
    custom_report, node_list, media, edit_profile, change_profile

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'admin/$', admin, name='admin'),
    url(r'overview/$', overview, name='overview'),
    url(r'daily_report/([0-9]*)/([0-9]*)?$', daily_report, name='daily_report'),
    url(r'weekly_reports/([0-9]*)/([0-9]*)?$', weekly_report, name='weekly_report'),
    url(r'monthly_report/([0-9]*)/([0-9]*)?$', monthly_report, name='monthly_report'),
    url(r'yearly_report/([0-9]*)/([0-9]*)?$', yearly_report, name='yearly_report'),
    url(r'custom_form/([0-9]*)/([0-9]*)?$', custom_form, name='custom_form'),
    url(r'custom_report/([0-9]*)/([0-9]*)?$', custom_report, name='custom_report'),
    url(r'media/$', media, name='media'),
    url(r'node_list/$', node_list, name='node_list'),
    url(r'profile', edit_profile, name='edit_profile'),
    url(r'change', change_profile, name='change_profile'),
]
