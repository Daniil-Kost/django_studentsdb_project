# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from students.models import Student, Group, Exam, Result
from django.contrib.auth.models import User
import random
from datetime import datetime, date


class Command(BaseCommand):
	args = '<model_name model_name ...>'
	help = "Prints to console name and number of created objects in a database."

	#Arrays with Students arguments

	first_names = [u'Юра', u'Виктор', u'Павло', u'Сергій',
	 u'Іван', u'Денис', u'Дмитро', u'Микола', u'Андрій',
		 u'Віталій', u'Олександр', u'Давид']

	last_names = [u'Юрьев', u'Петренко', u'Павловський', 
		u'Іллін', u'Іванов', u'Денисов',
		u'Макаров', u'Миколенко', u'Андрієнко', u'Подоба',
		 u'Олександров', u'Давидов']

	middle_names = [u'Юрійович', u'Петрович', u'Павлович', 
		u'Вікторович', u'Іванович', u'Денисович',
		u'Сергійович', u'Олегович', u'Андрійович', u'Виталійович',
		 u'Олександрович', u'Давидович']

	ticket = [u'15', u'27', u'33', u'44', u'50', u'77',
		u'88', u'12', u'22', u'30', u'7', u'5', u'2', u'3', u'1']

	#Arrays with Groups arguments

	title = [u'МтМ-12', u'МтМ-2', u'МтМ-3',
	 u'МтМ-4', u'МтМ-5', u'МтМ-9', u'МтМ-7',
	  u'МтМ-10', u'МтМ-15', u'МтМ-1']

	#Arrays with Exams arguments

	science = [u'Основи Python', u'Введення в ОПП', u'Основи HTML',
	 u'Введення в Java', u'Програмування з PHP',
	u'Django фреймворк', u'Введення в JavaScript']

	teacher_names = [u'Р.Г. Любавський', u'Д.В. Журавлев', 
	u'С.М. Куделко', u'І.П. Сергеєв',
	 u'К.В. Бардола', u'О.В. Ісаєва', u'М.В. Аласанія']

	#Arrays with Results arguments

	results = [u'50 балів - задовільно',
	 u'90 балів - відмінно', u'70 балів - добре']


	def handle(self, *args, **options):

		self.stdout.write(
			u'Function of automatic filling of the Database.' \
			u' How many objects need to create? ' )

		#students
		if 'students' in args:
			number = int(raw_input(
				u'Input the number of students: '))
			for i in range(number):
				student = Student(
					first_name = random.choice(self.first_names), 
					last_name = random.choice(self.last_names),
					middle_name = random.choice(self.middle_names), 
					ticket = random.choice(
						self.ticket) + random.choice(self.ticket),
					student_group = Group.objects.all()[random.randint(
						0, Group.objects.count()-1)],
					birthday =datetime.today())
				student.save()
				self.stdout.write(
					u'Objects %s create in database:' % student)

		#groups
		if 'groups' in args:
			number = int(raw_input(
				u'Input the number of groups: '))
			for i in range(number):
				group = Group(
					title = random.choice(self.title), 
					leader = Student.objects.all()[random.randint(
						0, Student.objects.count()-1)],)
				group.save()
				self.stdout.write(
					u'Objects %s create in database:' % group)

		#exams
		if 'exams' in args:
			number = int(raw_input(
				u'Input the number of exams: '))
			for i in range(number):
				exam = Exam(
					science = random.choice(self.science), 
					teacher = random.choice(self.teacher_names),
					date = datetime.today(), 
					groups = Group.objects.all()[random.randint(
						0, Group.objects.count()-1)])
				exam.save()
				self.stdout.write(
					u'Objects %s create in database:' % exam)

		#results
		if 'results' in args:
			number = int(raw_input(
				u'Input the number of exam results: '))
			for i in range(number):
				result = Result(
					exams = Exam.objects.all()[random.randint(
						0, Exam.objects.count()-1)], 
					groups = Group.objects.all()[random.randint(
						0, Group.objects.count()-1)],
					students = Student.objects.all()[random.randint(
						0, Student.objects.count()-1)], 
					result = random.choice(self.results))
				result.save()
				self.stdout.write(
					u'Objects %s create in database:' % result)
		