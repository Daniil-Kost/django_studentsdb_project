# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Student, Group, Exam, Result, MonthJournal
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

# Register your models here.

class StudentFormAdmin(ModelForm):

	def clean_student_group(self):
		"""Check if student leader in any group 

		If yes, then ensure it`s the same as selected group"""

		#get group where current student is a leader
		groups =Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(
				u'Студент є старостою іньшої  групи', code ='invalid')

		return self.cleaned_data['student_group']



class StudentAdmin(admin.ModelAdmin):

	list_display =['last_name', 'first_name', 'ticket',
		'student_group']
	list_display_links =['last_name', 'first_name']
	list_editable =['student_group']
	ordering =['last_name']
	list_filter =['student_group']
	list_per_page =10
	search_fields =['last_name', 'first_name', 'middle_name',
		'ticket', 'notes']

	form = StudentFormAdmin

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs ={'pk': obj.id})

#----------------------------------



class GroupAdmin(admin.ModelAdmin):

	list_display =['title', 'leader']
	list_display_links =['title', 'leader']
	ordering =['title']
	list_filter =['students']
	list_per_page =5
	search_fields =['title', 'leader', 'students', 'notes']


	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs ={'pk': obj.id})


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(MonthJournal)

