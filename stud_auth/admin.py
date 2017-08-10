# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User



#replace exciting User admin form

admin.site.register(User)
