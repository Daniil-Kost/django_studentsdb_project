# -*- coding: utf-8 -*-

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging

from .models import Student, Group, Exam, Result


# ---------------------------------------------------
# Student log
@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)",
                    student.first_name, student.last_name,
                    student.id)
    else:
        logger.info("Student updated: %s %s (ID: %d)",
                    student.first_name, student.last_name,
                    student.id)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)",
                student.first_name, student.last_name,
                student.id)


# -------------------------------------------------------
# Group log
@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group added: %s %s (ID: %d)",
                    group.title, group.leader, group.id)
    else:
        logger.info("Group updated: %s %s (ID: %d)",
                    group.title, group.leader, group.id)


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    logger.info("Group deleted: %s %s (ID: %d)",
                group.title, group.leader, group.id)


# -------------------------------------------------------
# Exam log
@receiver(post_save, sender=Exam)
def log_exam_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    exam = kwargs['instance']
    if kwargs['created']:
        logger.info("Exam added: %s %s (ID: %d)",
                    exam.science, exam.groups, exam.id)
    else:
        logger.info("Exam updated: %s %s (ID: %d)",
                    exam.science, exam.groups, exam.id)


@receiver(post_delete, sender=Exam)
def log_exam_deleted_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    exam = kwargs['instance']
    logger.info("Exam deleted: %s %s (ID: %d)",
                exam.science, exam.groups, exam.id)


# -------------------------------------------------------
# Result log
@receiver(post_save, sender=Result)
def log_result_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    result = kwargs['instance']
    if kwargs['created']:
        logger.info("Result added: %s %s (ID: %d)",
                    result.exams, result.students, result.id)
    else:
        logger.info("Result updated: %s %s (ID: %d)",
                    result.exams, result.students, result.id)


@receiver(post_delete, sender=Result)
def log_exam_deleted_event(sender, **kwargs):
    logger = logging.getLogger(__name__)

    result = kwargs['instance']
    logger.info("Result deleted: %s %s (ID: %d)",
                result.exams, result.students, result.id)
