'''This module contains the URL dispatcher for the Receiver application in 
the 'records' namespace'''

from django.conf.urls import url
from Receiver.views import overview, daily_report, weekly_report, monthly_report, yearly_report, custom_form, custom_report, report_list, node_list, node_status, get_actions, get_recent_actions

urlpatterns = [
    url(r'^$', overview, name='overview'),
    url(r'daily_report/([0-9]*)/([0-9]*)?$', daily_report, name='daily_report'),
    url(r'weekly_reports/([0-9]*)/([0-9]*)?$', weekly_report, name='weekly_report'),
    url(r'monthly_report/([0-9]*)/([0-9]*)?$', monthly_report, name='monthly_report'),
    url(r'yearly_report/([0-9]*)/([0-9]*)?$', yearly_report, name='yearly_report'),
    url(r'custom_form/([0-9]*)?$', custom_form, name='custom_form'),
    url(r'custom_report/$', custom_report, name='custom_report'),
    url(r'report_list/$', report_list, name='report_list'),
    url(r'node_list/$', node_list, name='node_list'),
    url(r'node_status/([0-9]*)?$', node_status, name='node_status'),
    url(r'scheduled_actions/$', get_actions, name='scheduled_actions'),
    url(r'recent_actions/$', get_recent_actions, name='recent_actions'),
]
