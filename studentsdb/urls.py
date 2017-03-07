"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.students import StudentAddView
from students.views.groups import GroupUpdateView, GroupDeleteView
from students.views.groups import GroupAddView
from students.views.exams import ExamUpdateView, ExamDeleteView
from students.views.exams import ExamAddView, ResultAddView
from students.views.exams import ResultUpdateView, ResultDeleteView
from students.views.journals import JournalView


js_info_dict ={
	'packages': ('students',),
}

urlpatterns = patterns('',

# Students urls
url(r'^$', 'students.views.students.students_list', name='home'),
url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),

url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
	name='students_edit'),

url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
 name='students_delete'),

#Journal ursl
url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name ='journal'),

#Groups urls
url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), 
	name='groups_edit'),
url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), 
	name='groups_delete'),


#Exams urls
url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
url(r'^exams/add/$', ExamAddView.as_view(), name='exams_add'),
url(r'^exams/(?P<pk>\d+)/edit/$', ExamUpdateView.as_view(), 
	name='exams_edit'),
url(r'^exams/(?P<pk>\d+)/delete/$', ExamDeleteView.as_view(),
 name='exams_delete'),


#Results urls
url(r'^exams/results/$', 
	'students.views.exams.exams_results', name='results'),
url(r'^exams/results/add/$', ResultAddView.as_view(), 
	name='results_add'),
url(r'^exams/results/(?P<pk>\d+)/edit/$', ResultUpdateView.as_view(),
 name='results_edit'),
url(r'^exams/results/(?P<pk>\d+)/delete/$', ResultDeleteView.as_view(),
 name='results_delete'),


#Contact admin urls
url(r'^contact-admin/$', 
	'students.views.contact_admin.contact_admin',
	 name='contact_admin'),

url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog',
	js_info_dict),

#url(r'^set-language/$',
 #       'students.views.set_language.set_language', name='set_language'),

url(r'^admin/', include(admin.site.urls)),



)

if DEBUG:
	#serve files from media folder
	urlpatterns +=patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': MEDIA_ROOT}))