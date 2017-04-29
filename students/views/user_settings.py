# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
import random
from ..models import Student, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from django import forms
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout
from crispy_forms.bootstrap import FormActions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from ..util import paginate, get_current_group
from .dispatch_view import Dispatch

def user_settings(request):
	return render(request, 'students/user_settings.html', {})