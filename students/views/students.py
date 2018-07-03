# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from ..models import Student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.forms import ModelForm
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from ..util import get_current_group
from .dispatch_view import Dispatch
from ..models import Page


class StudentsList(TemplateView):
    template_name = 'students/students_list.html'

    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(StudentsList, self).get_context_data(**kwargs)
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            students = Student.objects.filter(
                student_group=current_group)
        else:
            # otherwise show all students
            students = Student.objects.all()

        # try to order students list

        order_by = self.request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'ticket'):
            students = students.order_by(order_by)
        if self.request.GET.get('reverse', '') == '1':
            students = students.reverse()

        paginator = Paginator(students, 3)
        page = self.request.GET.get('page')
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        context['request'] = self.request

        context['students'] = students

        context['current_group'] = current_group

        context['order_by'] = order_by

        context['all_pages'] = Page.objects.all()

        for p in Page.objects.all():
            p.active_link = False
            p.save()

        return context


def my_page(request):
    # get request path (url)
    curr_path = request.path
    # get path without '/' (/test/) => test
    path = curr_path[1:len(curr_path) - 1]
    # get object from DB
    page = Page.objects.get(url_field=path)

    other_pages = Page.objects.exclude(url_field=path)

    page.active_link = True
    page.save()

    for p in other_pages:
        p.active_link = False
        p.save()

    all_pages = Page.objects.all()

    return render(request, 'students/test_page.html', {
        'page': page, 'other_pages': other_pages,
        'all_pages': all_pages})


class PageUpdateForm(ModelForm):
    class Meta:
        model = Page

        exclude = ("",)

    def __init__(self, *args, **kwargs):
        super(PageUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set from tag attributes
        self.helper.form_action = reverse('page',
                                          kwargs={'slug': kwargs['instance'].slug})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'


class PageUpdateView(SuccessMessageMixin, Dispatch, UpdateView):
    """docstring for StudentUpdateView"""

    model = Page
    template_name = 'students/test_page.html'

    exclude = ("",)

    form_class = PageUpdateForm

    success_url = '/'
    success_message = _(u"Student %(first_name)s %(last_name)s saved succesfully !")

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        # get request path (url)
        curr_path = self.request.path
        # remove /page path in url
        short_path = curr_path.split('/page')
        # get path variable from short_path list
        my_path = short_path[1]
        # get path without '/' (/test/) => test
        path = my_path[1:len(my_path) - 1]
        # get object from DB
        page = Page.objects.get(url_field=path)

        other_pages = Page.objects.exclude(url_field=path)

        page.active_link = True
        page.save()

        for p in other_pages:
            p.active_link = False
            p.save()

        all_pages = Page.objects.all()
        context['page'] = page
        context['other_pages'] = other_pages
        context['all_pages'] = all_pages
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(
                PageUpdateView, self).post(request, *args, **kwargs)


class StudentAddForm(ModelForm):
    class Meta:
        model = Student

        exclude = ("",)

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set from tag attributes
        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # self.helper.render_unmentioned_fields = True

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-4 control label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', _(u'Save'),
                   css_class="btn save btn-primary"),
            Submit('student_cancel_button', _(u'Cancel'),
                   css_class="btn cancel btn-danger"), ))


class StudentAddView(SuccessMessageMixin, Dispatch, CreateView):
    """docstring for ContactForm"""

    model = Student
    template_name = 'students/students_edit.html'
    exclude = ("",)

    form_class = StudentAddForm

    success_url = '/'
    success_message = _(u"Student %(first_name)s %(last_name)s added succesfully !")

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
        model = Student

        exclude = ("",)

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set from tag attributes
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-4 control label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', _(u'Save'),
                   css_class="btn save btn-primary"),
            Submit('cancel_button', _(u'Cancel'),
                   css_class="btn cancel btn-danger"), ))


class StudentUpdateView(SuccessMessageMixin, Dispatch, UpdateView):
    """docstring for StudentUpdateView"""

    model = Student
    template_name = 'students/students_edit.html'

    exclude = ("",)

    form_class = StudentUpdateForm

    success_url = '/'
    success_message = _(u"Student %(first_name)s %(last_name)s saved succesfully !")

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(
                StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(SuccessMessageMixin, Dispatch, DeleteView):
    """docstring for StudentDeleteView"""
    model = Student
    template_name = 'students/students_delete.html'

    success_url = reverse_lazy('home')
    success_message = _(u"Student succesfully deleted !")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)
