# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
import random
from ..models import Group
from ..models import Student
from ..models import Exam
from ..models import Result
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from django import forms
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from ..util import paginate, get_current_group
from django.utils.translation import ugettext as _


def exams_list(request):

	current_group =get_current_group(request)
	if current_group:
		exams =Exam.objects.filter(
			gr=current_group)
	else:
		#otherwise show all students
		exams =Exam.objects.all()


	#paginate exams

	context =paginate(exams, 4, request, {}, var_name='exams')
		
	return render(request, 'students/exams_list.html', context)


class ExamAddForm(ModelForm):

	class Meta:
		model =Exam

		#fields ="__all__"
		exclude=("",)
		
	def __init__(self, *args, **kwargs):
		super(ExamAddForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('exams_add')
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
			Submit('exam_cancel_button', _(u'Cancel'),
				css_class ="btn btn-danger"))


class ExamAddView(SuccessMessageMixin, CreateView):

	model =Exam
	template_name ='students/exams_edit.html'
	exclude=("",)


	form_class =ExamAddForm
	
	success_url = '/exams/'
	success_message =_(u"Exam %(science)s (%(gr)s) succesfully added !")

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(
				ExamAddView, self).post(request, *args, **kwargs)
	


class ExamUpdateForm(ModelForm):

	class Meta:
		model =Exam

		exclude=("",)
		#fields ="__all__"
		
	def __init__(self, *args, **kwargs):
		super(ExamUpdateForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('exams_edit', 
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



class ExamUpdateView(SuccessMessageMixin, UpdateView):
	"""docstring for ExamUpdateView"""
	model =Exam
	template_name ='students/exams_edit.html'

	exclude=("",)

	form_class =ExamUpdateForm

	success_url = '/exams/'
	success_message =_(u"Exam %(science)s (%(gr)s) succesfully saved !")


	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(
				ExamUpdateView, self).post(request, *args, **kwargs)
	
		
class ExamDeleteView(SuccessMessageMixin, DeleteView):
	"""docstring for ExamDeleteView"""
	model =Exam
	template_name ='students/exams_delete.html'

	success_url = reverse_lazy('exams')
	success_message =_(u"Exam succesfully deleted !")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(ExamDeleteView, self).delete(request, *args, **kwargs)


#-------------------------------------


def exams_results(request):

	current_group =get_current_group(request)
	if current_group:
		results =Result.objects.filter(
			groups=current_group)
	else:
		#otherwise show all students
		results =Result.objects.all()

	#try to order exams result

	order_by =request.GET.get('order_by', '')
	if order_by in ('exams', 'groups', 'students', 'results_exam'):
		results =results.order_by(order_by)
		if request.GET.get('reverse', '' ) =='1':
			results =results.reverse()


	#paginate results

	context =paginate(results, 4, request, {}, var_name='results')


	return render(request, 'students/exams_result.html',  context)


class ResultAddForm(ModelForm):

	class Meta:
		model =Result

		#fields ="__all__"
		exclude=("",)
		
	def __init__(self, *args, **kwargs):
		super(ResultAddForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('results_add')
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
			Submit('result_cancel_button', _(u'Cancel'),
				css_class ="btn btn-danger"))


class ResultAddView(SuccessMessageMixin, CreateView):

	model =Result
	template_name ='students/results_edit.html'
	exclude=("",)


	form_class =ResultAddForm

	success_url = '/exams/results/'
	success_message =_(u"Exam result %(exams)s (%(students)s) succesfully added !")


	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('results'))
		else:
			return super(
				ResultAddView, self).post(request, *args, **kwargs)
	


class ResultUpdateForm(ModelForm):

	class Meta:
		model =Result

		exclude=("",)
		#fields ="__all__"
		
	def __init__(self, *args, **kwargs):
		super(ResultUpdateForm, self).__init__(*args, **kwargs)

		self.helper =FormHelper(self)

		#set from tag attributes
		self.helper.form_action =reverse('results_edit', 
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



class ResultUpdateView(SuccessMessageMixin, UpdateView):
	"""docstring for ExamUpdateView"""
	model =Result
	template_name ='students/results_edit.html'

	exclude=("",)

	form_class =ResultUpdateForm

	success_url = '/exams/results/'
	success_message =_(u"Exam result %(exams)s %(students)s succesfully saved !")


	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('results'))
		else:
			return super(
				ResultUpdateView, self).post(request, *args, **kwargs)
	
		
class ResultDeleteView(SuccessMessageMixin, DeleteView):
	"""docstring for ExamDeleteView"""
	model =Result
	template_name ='students/results_delete.html'

	success_url = reverse_lazy('results')
	success_message =_(u"Exam result succesfully deleted !")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(ResultDeleteView, self).delete(request, *args, **kwargs)
