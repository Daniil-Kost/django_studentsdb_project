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
from django.utils.translation import ugettext as _



def students_list(request):

	#check if we need to show only one group of students
	current_group =get_current_group(request)
	if current_group:
		students =Student.objects.filter(
			student_group=current_group)
	else:
		#otherwise show all students
		students =Student.objects.all()

	#try to order students list

	order_by =request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students =students.order_by(order_by)
		if request.GET.get('reverse', '' ) =='1':
			students =students.reverse()

	#apply pagination, 3 students per page
	context =paginate(students, 3, request, {}, var_name='students')

	return render(request, 'students/students_list.html', context)

class StudentAddForm(ModelForm):

	class Meta:
		model =Student

		#fields ="__all__"
		exclude=("",)
		
	def __init__(self, *args, **kwargs):
		super(StudentAddForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('students_add')
		self.helper.form_method ='POST'
		self.helper.form_class ='form-horizontal'
		#self.helper.render_unmentioned_fields = True

		#set form field properties
		self.helper.help_text_inline =True
		self.helper.html5_required =True
		self.helper.label_class ='col-sm-4 control label'
		self.helper.field_class ='col-sm-8'

		#add buttons
		self.helper.layout[-1] =FormActions(
			Submit('add_button', _(u'Save'),
			 css_class ="btn btn-primary"),
			Submit('student_cancel_button', _(u'Cancel'),
				css_class ="btn btn-danger"),)
		

class StudentAddView(SuccessMessageMixin, CreateView):
	"""docstring for ContactForm"""

	model =Student
	template_name ='students/students_edit.html'
	exclude=("",)

	form_class =StudentAddForm
	
	success_url = '/'
	success_message =_(u"Student %(first_name)s %(last_name)s added succesfully !")

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(
				u'%s?status_message=%s' % reverse(
			'home', _(u'Student add canceled !')))
		else:
			return super(
				StudentAddView, self).post(request, *args, **kwargs)
	


class StudentUpdateForm(ModelForm):

	class Meta:
		model =Student

		exclude=("",)
		#fields ="__all__"
		
	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('students_edit', 
			kwargs ={'pk': kwargs['instance'].id})
		self.helper.form_method ='POST'
		self.helper.form_class ='form-horizontal'

		#set form field properties
		self.helper.help_text_inline =True
		self.helper.html5_required =True
		self.helper.label_class ='col-sm-4 control label'
		self.helper.field_class ='col-sm-8'

		#add buttons
		self.helper.layout[-1] =FormActions(
			Submit('add_button', _(u'Save'),
			 css_class ="btn btn-primary"),
			Submit('cancel_button', _(u'Cancel'),
				css_class ="btn btn-danger"),)



class StudentUpdateView(SuccessMessageMixin, UpdateView):
	"""docstring for StudentUpdateView"""
	model =Student
	template_name ='students/students_edit.html'

	exclude=("",)

	form_class =StudentUpdateForm

	success_url = '/'
	success_message =_(u"Student %(first_name)s %(last_name)s saved succesfully !")

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(
				StudentUpdateView, self).post(request, *args, **kwargs)
	
		
class StudentDeleteView(SuccessMessageMixin, DeleteView):
	"""docstring for StudentDeleteView"""
	model =Student
	template_name ='students/students_delete.html'

	success_url = reverse_lazy('home')
	success_message =_(u"Student succesfully deleted !")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(StudentDeleteView, self).delete(request, *args, **kwargs)
