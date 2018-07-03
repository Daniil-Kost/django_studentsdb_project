# -*- coding: utf-8 -*-

from django.shortcuts import render


def user_settings(request):
    return render(request, 'students/user_settings.html', {})
