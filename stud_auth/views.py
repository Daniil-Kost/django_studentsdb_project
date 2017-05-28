# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django import forms
from django.views.generic import CreateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout
from crispy_forms.bootstrap import FormActions
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from models import StProfile
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from students.util import paginate

from registration.forms import RegistrationForm
from registration.forms import RegistrationFormUniqueEmail
from registration.forms import RegistrationFormNoFreeEmail
from registration.views import RegistrationView
from registration.views import ActivationView

from django.contrib.auth.models import User

# Create your views here.

def users_list(request):

	users = User.objects.all()

	#apply pagination, 10 users per page
	context = paginate(users, 10, request, {}, var_name = 'users')

	return render(request, 'registration/users_list.html', 
		context)


class ProfileForm(ModelForm):

	class Meta:
		model = User

		exclude = ("",)
		#fields ="__all__"
		
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set from tag attributes
		self.helper.form_action = reverse('user_profile', 
			kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'


class ProfileView(SuccessMessageMixin, UpdateView):
	"""docstring for ProfileView"""

	model = User
	template_name = 'registration/user_profile.html'

	exclude = ("",)

	form_class = ProfileForm

	success_url = '/'
	
	def post(self, request, *args, **kwargs):
		if request.POST.get('home_button'):
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(
				ProfileView, self).post(request, *args, **kwargs)


class ProfileFormEdit(ModelForm):

	class Meta:
		model = User

		#exclude = ("",)
		fields = ("first_name", "last_name", "email",)
		
	def __init__(self, *args, **kwargs):
		super(ProfileFormEdit, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set from tag attributes
		self.helper.form_action = reverse('profile_edit', 
			kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		#set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control label'
		self.helper.field_class = 'col-sm-8'

		#add buttons
		self.helper.layout.append(FormActions(
			Submit('user_add_button', _(u'Save'),
			 css_class = "btn edit btn-primary"),
			Submit('cancel_button', _(u'Cancel'),
				css_class = "btn e-cancel btn-danger"),))


class ProfileViewEdit(SuccessMessageMixin, UpdateView):
	"""docstring for ProfileViewEdit"""

	model = User
	template_name = 'registration/user_edit.html'

	#exclude = ("",)

	form_class = ProfileFormEdit

	success_url = '/accounts/users'

	success_message = _(u"User updated succesfully !")
	

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect(reverse('users'))
		else:
			return super(
				ProfileViewEdit, self).post(request, *args, **kwargs)


class UserDeleteView(SuccessMessageMixin, DeleteView):
	"""docstring for UserDeleteView"""

	model = User
	template_name = 'registration/user_delete.html'

	success_url = reverse_lazy('users')

	success_message = _(u"User succesfully deleted !")

	def delete(self, request, *args, **kwargs):
		return super(UserDeleteView, self).delete(request, *args, **kwargs)


#-----------------------------------------------
#Registration
class UserRegistrationForm(RegistrationForm):
	"""docstring for UserRegistrationForm"""
	class Meta:
		model = User

		fields = ("username", "first_name", "last_name", "email",
			"password1", "password2", "date_joined", )
		#exclude = ("",)
		#fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set from tag attributes
		self.helper.form_action = reverse('users:registration_register')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.render_unmentioned_fields = True

		#set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-4 control label'
		self.helper.field_class = 'col-sm-8'

		#add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', _(u'Save'),
				css_class = "btn save btn-primary"),
			Submit('student_cancel_button', _(u'Cancel'),
				css_class = "btn cancel btn-danger"),))


class UserRegistrationView(RegistrationView):
	"""docstring for UserRegistrationView"""

	form_class = UserRegistrationForm

	success_url = '/'

	disallowed_url = '/accounts/register/'

	template_name = 'registration/registration_form.html'

	def post(self, request, *args, **kwargs):

			return super(
				UserRegistrationView, self).post(request, *args, **kwargs)





			