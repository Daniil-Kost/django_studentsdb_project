# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Dispatch(object):
	"""docstring for Dispatch"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		
		return super(Dispatch, self).dispatch(*args, **kwargs)