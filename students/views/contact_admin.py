# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from studentsdb.settings import ADMIN_EMAIL
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import random
from ..models import Group
from ..models import Student
from ..models import Exam
from ..models import Result
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import pdb
import logging
from django.utils.translation import ugettext as _



class ContactForm(forms.Form):
	"""docstring for ContactForm"""

	def __init__(self, *args, **kwargs):
		#call original initializator
		super(ContactForm, self).__init__(*args, **kwargs)

		#this helper object allows us to us to customize form
		self.helper =FormHelper()

		#form tag attributes
		self.helper.form_class ='form-horizontal'
		self.helper.form_method ='post'
		self.helper.form_action =reverse('contact_admin')

		#twitter bootstrap styles
		self.helper.help_text_inline =True
		self.helper.html5_required =True
		self.helper.label_class ='col-sm-2 control label'
		self.helper.field_class ='col-sm-10'

		#from buttons
		self.helper.add_input(Submit('send_button', _(u"Send")))


	from_email =forms.EmailField(label =_(u"Your email adress"))

	subject =forms.CharField(
		label =_(u"Title"),
		max_length =128)

	message =forms.CharField(
		label =_(u"Text message"),
		widget =forms.Textarea)
		
		
def contact_admin(request):

	if request.method =='POST':
		form =ContactForm(request.POST)

		if form.is_valid():
			subject =form.cleaned_data['subject']
			message =form.cleaned_data['message']
			from_email =form.cleaned_data['from_email']

			try:
				send_mail(subject, message, from_email, [ADMIN_EMAIL])

			except Exception:
				#message =u'Під час відправки виникла непередбачувана' \
				#u' помилка. Спробуйте скористатись данною формою пізніше.'

				message = _(u"When you send an unexpected error occurred. Try this form later.")


				logger =logging.getLogger(__name__)
				logger.exception(message)
				#pdb.set_trace()
				#pdb.pm()


			else:
				#message =u'Повідомлення успішно надіслане !'
				message = _(u"Message sent successfully !")

			return HttpResponseRedirect(
				u'%s?status_message=%s' % (reverse('contact_admin'), message))

	else:
		form =ContactForm()

	return render(request, 'students/contact_admin.html', {'form': form})


