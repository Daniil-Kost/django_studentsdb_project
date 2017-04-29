# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
import random
from ..models import Group
from ..models import Student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView
from django.forms import ModelForm
from django import forms
from django.views.generic import UpdateView, CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Button, HTML
from crispy_forms.bootstrap import FormActions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from ..util import paginate, get_current_group
from django.utils.translation import ugettext as _
from .dispatch_view import Dispatch

def groups_list(request):

	current_group = get_current_group(request)
	if current_group:
		groups = Group.objects.filter(
			title = current_group)
	else:
		#otherwise show all groups
		groups = Group.objects.all().order_by('title')

	#paginate groups

	context = paginate(groups, 4, request, {}, var_name = 'groups')
		
	return render(request, 'students/groups_list.html', context)


class GroupAddForm(ModelForm):

	class Meta:
		model = Group

		#fields ="__all__"
		exclude = ("",)
		
	def __init__(self, *args, **kwargs):
		super(GroupAddForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set from tag attributes
		self.helper.form_action = reverse('groups_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		#set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control label'
		self.helper.field_class = 'col-sm-8'

		#add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', _(u'Save'),
				css_class = "btn btn-primary"),
			Submit('group_cancel_button', _(u'Cancel'),
				css_class = "btn btn-danger")))


class GroupAddView(SuccessMessageMixin, Dispatch, CreateView):

	model = Group
	template_name = 'students/groups_edit.html'
	exclude = ("",)

	form_class = GroupAddForm
	
	success_url = '/groups/'
	success_message = _(u"Group %(title)s succesfully added !")
		

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(
				GroupAddView, self).post(request, *args, **kwargs)
	


class GroupUpdateForm(ModelForm):

	class Meta:
		model = Group

		exclude = ("",)
		#fields ="__all__"

	def __init__(self, *args, **kwargs):
		super(GroupUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set from tag attributes
		self.helper.form_action = reverse('groups_edit', 
			kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		#set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control label'
		self.helper.field_class = 'col-sm-8'

		#add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', _(u'Save'),
			 css_class = "btn btn-primary"),
			Submit('cancel_button', _(u'Cancel'),
				css_class = "btn btn-danger"),))



class GroupUpdateView(SuccessMessageMixin, Dispatch, UpdateView):
	"""docstring for GroupUpdateView"""
	model = Group
	template_name = 'students/groups_edit.html'

	exclude = ("",)

	form_class = GroupUpdateForm

	success_url = '/groups/'
	success_message = _(u"Group %(title)s succesfully saved !")
 

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse(
			'groups'))
		else:
			return super(
				GroupUpdateView, self).post(request, *args, **kwargs)
	
		
class GroupDeleteView(SuccessMessageMixin, Dispatch, DeleteView):
	"""docstring for GroupDeleteView"""
	model = Group
	template_name = 'students/groups_delete.html'

	success_url = reverse_lazy('groups')
	success_message = _(u"Group succesfully deleted !")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(GroupDeleteView, self).delete(request, *args, **kwargs)



	
