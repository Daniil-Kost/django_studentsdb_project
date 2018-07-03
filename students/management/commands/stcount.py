# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from students.models import Student, Group, Exam, Result
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = "Prints to console number of related objects in a database."

    models = (
        ('students', Student), ('groups', Group), ('users', User),
        ('exams', Exam), ('results', Result)
    )

    def handle(self, *args, **options):
        for name, model in self.models:
            if name in args:
                self.stdout.write(
                    'Number of %s in database: %d' % (
                        name, model.objects.count()))
