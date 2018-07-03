# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'
    verbose_name = u'База Студентів'

    def ready(self):
        from students import signals




