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
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.students import StudentAddView
from students.views.groups import GroupUpdateView, GroupDeleteView
from students.views.groups import GroupAddView, groups_list
from students.views.exams import ExamUpdateView, ExamDeleteView
from students.views.exams import ExamAddView, ResultAddView, exams_results
from students.views.exams import ResultUpdateView, ResultDeleteView
from students.views.journals import JournalView
from django.contrib.auth.decorators import login_required
from stud_auth.views import UserRegistrationView, UserRegistrationForm
from stud_auth.views import ProfileView, ProfileViewEdit
from stud_auth.views import UserDeleteView
js_info_dict = {
	'packages': ('students',),
}

urlpatterns = [


# Students urls
url(r'^$', 'students.views.students.students_list', 
	name = 'home'),
url(r'^students/add/$', login_required(StudentAddView.as_view()), 
	name = 'students_add'),

url(r'^students/(?P<pk>\d+)/edit/$', login_required(
	StudentUpdateView.as_view()),
	name = 'students_edit'),

url(r'^students/(?P<pk>\d+)/delete/$', login_required(
	StudentDeleteView.as_view()),
	name = 'students_delete'),


#Journal ursl
url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(),
	name = 'journal'),


#Groups urls
url(r'^groups/$', 'students.views.groups.groups_list',
	name = 'groups'),
url(r'^groups/add/$', login_required(GroupAddView.as_view()), 
	name = 'groups_add'),
url(r'^groups/(?P<pk>\d+)/edit/$', 
	login_required(GroupUpdateView.as_view()), 
	name = 'groups_edit'),
url(r'^groups/(?P<pk>\d+)/delete/$', 
	login_required(GroupDeleteView.as_view()), 
	name = 'groups_delete'),


#Exams urls
url(r'^exams/$', 'students.views.exams.exams_list', 
	name = 'exams'),
url(r'^exams/add/$', login_required(ExamAddView.as_view()), 
	name = 'exams_add'),
url(r'^exams/(?P<pk>\d+)/edit/$', login_required(
	ExamUpdateView.as_view()), 
	name = 'exams_edit'),
url(r'^exams/(?P<pk>\d+)/delete/$', login_required(
	ExamDeleteView.as_view()),
	name = 'exams_delete'),


#Results urls
url(r'^exams/results/$', exams_results, 
	name = 'results'),
url(r'^exams/results/add/$', login_required(
	ResultAddView.as_view()), 
	name = 'results_add'),
url(r'^exams/results/(?P<pk>\d+)/edit/$', login_required(
	ResultUpdateView.as_view()),
	name = 'results_edit'),
url(r'^exams/results/(?P<pk>\d+)/delete/$', login_required(
	ResultDeleteView.as_view()),
	name = 'results_delete'),


#Contact admin urls
url(r'^contact-admin/$', 
	'students.views.contact_admin.contact_admin',
	name = 'contact_admin'),


#User Releted urls
url(r'^accounts/my-profile/$', login_required(TemplateView.as_view(
	template_name = 'registration/profile.html')),
	name = 'profile'),
url(r'^accounts/profile/(?P<pk>\d+)/$', login_required(
	ProfileView.as_view()),
	name = 'user_profile'),
url(r'^accounts/profile/(?P<pk>\d+)/edit/$', login_required(
	ProfileViewEdit.as_view()),
	name = 'profile_edit'),

url(r'^users/logout/$', auth_views.logout, 
	kwargs = {'next_page': 'home'}, 
	name = 'auth_logout'),
url(r'^register/complete/$', 
	RedirectView.as_view(pattern_name = 'home'), 
	name = 'registration_complete'),
url(r'^users/', include('registration.backends.simple.urls',
	namespace = 'users')),
url(r'^accounts/register/$',
	UserRegistrationView.as_view(),
    name = 'register',),

url(r'^accounts/users/$', 'stud_auth.views.users_list',
    name = 'users',),
url(r'^accounts/profile/(?P<pk>\d+)/delete/$', login_required(
	UserDeleteView.as_view()),
	name = 'user_delete'),


#User Settings
url(r'^settings/$', 'students.views.user_settings.user_settings', 
	name = 'user_settings'),


#Social Auth Related urls
url('^social/', include('social.apps.django_app.urls',
	namespace='social')),


url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog',
	js_info_dict),
url(r'^admin/', include(admin.site.urls)),



]

if DEBUG:
	#serve files from media folder
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': MEDIA_ROOT}))