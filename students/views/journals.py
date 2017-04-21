# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
import random
from ..models import Student, MonthJournal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from django.http import JsonResponse
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from django import forms
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.base import TemplateView
from ..util import paginate, get_current_group
import pdb;
from django.utils.translation import ugettext as _

class JournalView(TemplateView):
    template_name = 'students/journal_list.html'

    def get_context_data(self, **kwargs):
		#get context data from TemplateView class
		context = super(JournalView, self).get_context_data(**kwargs)

		#перевіряємо чи передали нам місяць в параметрі
		if self.request.GET.get('month'):
			month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
		else:
			#якщо ні - вичисляємо поточний;
			today = datetime.today()
			month = date(today.year, today.month, 1)

		today = datetime.today()

		#обчислюємо поточний рік, попередній і наступний місяці
		#we need this for month navigation element in template
		next_month = month + relativedelta(months = 1)
		prev_month = month - relativedelta(months = 1)
		context['prev_month'] = prev_month.strftime('%Y-%m-%d')
		context['next_month'] = next_month.strftime('%Y-%m-%d')
		context['year'] = month.year
		#також поточний місяць;
		#змінну cur_month ми використовуватимемо пізніше
		#в пагінації; а month_verbose 
		#в навігації помісячній
		context['cur_month'] = month.strftime('%Y-%m-%d')
		context['month_verbose'] = month.strftime('%B')

		myear = month.year
		mmonth = month.month
		number_of_days = monthrange(myear, mmonth)[1]
		#передаємо в контекст список днів для заголовку 
		#таблиці із відвідування. 
		#передаємо в контекст список днів
		#для заголовку таблиці із відвідуванням; 
		#для цього користуємось можливістю динамічно створювати
		#список з допомогою вкладеного циклу 
		#(так звані List Comprehensions в Python); 
		#в циклі ми пробігаємось по списку 
		#днів у місяці і запам’ятовуємо його 
		#під ключем ‘day’ в словнику; для кожного дня 
		#отримуємо його порядковий номер в тижні (з допомогою
		#функції weekday), а вже тоді
		#його назву із словника day_abbr; отриману
		#назву обрізаємо до двох символів
		#та запам’ятовуємо в словнику під ключем ‘verbose’
		context['month_header'] = [
			{'day':d, 'verbose': day_abbr[weekday(myear,
				mmonth, d)][:3]}
			for d in range(1, number_of_days+1)]

		#витягуємо усіх студентів по сортованих по прізвищу
		#або одного студента за id
		if kwargs.get('pk'):
			queryset = [Student.objects.get(pk = kwargs['pk'])]
		else:
			current_group = get_current_group(self.request)
			if current_group:
				queryset = Student.objects.filter(
					student_group = current_group)
			else:
				queryset = Student.objects.all().order_by('last_name')

		#це адреса для посту AJAX запиту, як бачите, ми
		#робитимемо його на цю ж вʼюшку; вьюшка журналу
		#буде і показувати журнал і обслуговувати запити
		#типу пост на оновлення журналу

		update_url = reverse('journal')

		#пробігаємось по усіх студентах і збираємо 
		#необхідні дані
		students = []
		for student in queryset:
			#TODO: витягуємо журнал для студента і
			#вибраного місяця
			try:
				journal = MonthJournal.objects.get(
					student = student, date = month)
			except Exception:
				journal = None

			#набиваємо дні для студента
			days = []
			for day in range(1, number_of_days+1):
				days.append({
					'day': day,
					'present' : journal and getattr(journal,
						'present_day%d' % day, False) or False, 
					'date': date(myear, mmonth, day).strftime(
						'%Y-%m-%d'),
					})

			#студент
			students.append({
				'fullname': u'%s %s' % (student.last_name,
				 student.first_name),
				'days': days,
				'id': student.id,
				'update_url' :update_url,
				})

		#застосовуємо пагінацію до списку студентів
		context = paginate(students, 10, self.request, context,
				var_name ='students')

		return context 


    def post(self, request, *args, **kwargs):
		data = request.POST

		current_date = datetime.strptime(data['date'], 
			'%Y-%m-%d').date()
		#pdb.set_trace()
		#pdb.pm()
		month = date(current_date.year, current_date.month, 1)
		present = data['present'] and True or False
		student = Student.objects.get(pk = data['pk'])

		#get or create journal object for given student and month
		journal = MonthJournal.objects.get_or_create(student = student,
			date = month)[0]

		#set new presence on journal for given student and save result
		setattr(journal, 'present_day%d' % current_date.day, present)
		journal.save()

		#return success status
		return JsonResponse({'status': 'success'})

