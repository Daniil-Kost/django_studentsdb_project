# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from datetime import datetime
from django.utils.translation import ugettext_lazy as _


#Create your models here.

class Student(models.Model):
	"""Student Model"""

	class Meta(object):
		"""docstring for Meta"""
		verbose_name =_(u"Student")
		verbose_name_plural =_(u"Students")
			
	first_name = models.CharField(
		max_length =256,
		blank =False,
		verbose_name =_(u"Name"))

	last_name = models.CharField(
		max_length =256,
		blank =False,
		verbose_name =_(u"Last Name"))

	middle_name = models.CharField(
		max_length =256,
		blank =True,
		verbose_name =_(u"Middle Name"),
		default ='')

	birthday = models.DateField(
		blank =False,
		verbose_name =_(u"Birthday"),
		null =True)

	photo = models.ImageField(
		blank =True,
		verbose_name =_(u"Photo"),
		null =True)

	ticket = models.CharField(
		max_length =256,
		blank =False,
		verbose_name =_(u"Ticket"))

	student_group = models.ForeignKey('Group',
		verbose_name =_(u"Group"),
		blank =False,
		null =True,
		on_delete =models.PROTECT)

	notes =models.TextField(
		blank = True,
		verbose_name =_(u"Notes"))

	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)

#--------------------------------------------------------------
class Group(models.Model):
	"""Group Model"""

	class Meta(object):
		"""docstring for Meta"""
		verbose_name =_(u"Group")
		verbose_name_plural =_(u"Groups")
			
	title = models.CharField(
		max_length =256,
		blank =False,
		verbose_name = _(u"Name"))

	leader = models.OneToOneField('Student',
		verbose_name =_(u"Leader"),
		blank =True,
		null =True,
		on_delete =models.SET_NULL,
		related_name='+')

	students = models.ManyToManyField('Student',
		verbose_name =_(u"Students"), 
		blank =True,)

	notes = models.TextField(
		blank = True,
		verbose_name =_(u"Notes"))

	def __unicode__(self):
			return u"%s" % (self.title)

#------------------------------------------------

class Exam(models.Model):
	"""Exam Model"""

	class Meta(object):
		"""docstring for Meta"""
		verbose_name =_(u"Exam")
		verbose_name_plural =_(u"Exams")
			
	science = models.CharField(
		max_length =256,
		blank =False,
		verbose_name =_(u"Science"))

	teacher = models.CharField(
		max_length =256,
		blank =False,
		verbose_name =_(u"Teacher"))

	date = models.DateTimeField(
		blank =False,
		verbose_name =_(u"Time"),
		null =True)

	group = models.ForeignKey('Group',
		verbose_name =_(u"Group"),
		blank =False,
		null =True,
		on_delete =models.CASCADE)

	def __unicode__(self):
		return u"%s (%s)" % (self.science, self.group)

#-----------------------------------------------------------


class Result(models.Model):

	"""Result Model"""

	class Meta(object):
		"""docstring for Meta"""
		verbose_name =_(u"Exam Result")
		verbose_name_plural =_(u"Exams Results")
			
	exam = models.ForeignKey('Exam',
		verbose_name = _(u"Exam"),
		blank =False,
		null =True,
		max_length =256,
		on_delete =models.CASCADE)

	group = models.ForeignKey('Group',
		verbose_name =_(u"Group"),
		blank =False,
		null =True,
		on_delete =models.CASCADE)

	student = models.ForeignKey('Student',
		verbose_name =_(u"Student"),
		blank =False,
		null =True,
		on_delete =models.CASCADE,
		related_name='+')

	result = models.CharField(
		max_length =256,
		blank =False,
		verbose_name = _(u"Result"))

	def __unicode__(self):
		return u"%s %s" % (self.exams, self.students)


#----------------------------------------------------------------

class MonthJournal(models.Model):
    """Student Month Journal"""

    class Meta:
        verbose_name =_(u"Monthly Journal")
        verbose_name_plural =_(u"Mounthly Journals")

    student = models.ForeignKey('Student',
        verbose_name=_(u"Student"),
        blank=False,
        unique_for_month='date')

    # we only need year and month, so always set day to first day of the month
    date = models.DateField(
        verbose_name=_(u"Date"),
        blank=False,
        default =datetime.today)

    # list of days, each says whether student was present or not
    present_day1 = models.BooleanField(default=False)
    present_day2 = models.BooleanField(default=False)
    present_day3 = models.BooleanField(default=False)
    present_day4 = models.BooleanField(default=False)
    present_day5 = models.BooleanField(default=False)
    present_day6 = models.BooleanField(default=False)
    present_day7 = models.BooleanField(default=False)
    present_day8 = models.BooleanField(default=False)
    present_day9 = models.BooleanField(default=False)
    present_day10 = models.BooleanField(default=False)
    present_day11 = models.BooleanField(default=False)
    present_day12 = models.BooleanField(default=False)
    present_day13 = models.BooleanField(default=False)
    present_day14 = models.BooleanField(default=False)
    present_day15 = models.BooleanField(default=False)
    present_day16 = models.BooleanField(default=False)
    present_day17 = models.BooleanField(default=False)
    present_day18 = models.BooleanField(default=False)
    present_day19 = models.BooleanField(default=False)
    present_day20 = models.BooleanField(default=False)
    present_day21 = models.BooleanField(default=False)
    present_day22 = models.BooleanField(default=False)
    present_day23 = models.BooleanField(default=False)
    present_day24 = models.BooleanField(default=False)
    present_day25 = models.BooleanField(default=False)
    present_day26 = models.BooleanField(default=False)
    present_day27 = models.BooleanField(default=False)
    present_day28 = models.BooleanField(default=False)
    present_day29 = models.BooleanField(default=False)
    present_day30 = models.BooleanField(default=False)
    present_day31 = models.BooleanField(default=False)

    def __getitem__(self, key):
    	return self.date[key]

    def __unicode__(self):
        return u'%s: %d, %d' % (self.student.last_name,
         self.date.month, self.date.year)
