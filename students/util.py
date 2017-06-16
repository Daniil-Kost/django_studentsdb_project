# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from studentsdb.settings import LANGUAGE_CODE

def paginate(objects, size, request, context, var_name='object_list'):
	"""Paginate objects provided by view"""

	#apply pagination
	paginator =Paginator(objects, size)

	#try to get page number from request
	page =request.GET.get('page', '1')
	try:
		object_list =paginator.page(page)

	except PageNotAnInteger:
		#if page is not at integer, deliver first page
		object_list =paginator.page(1)

	except EmptyPage:
		#if page is out of range
		#deliver last page of results
		object_list =paginator.page(paginator.num_pages)

	#set variables into context
	context[var_name] =object_list
	context['is_paginated'] =object_list.has_other_pages()
	context['page_obj'] =object_list
	context['paginator'] =paginator

	return context

def get_groups(request):
	"""Returns list of existing groups"""
	#deferred import of Group model to avoid cycled imports
	from .models import Group

	#get currently selected group
	cur_group =get_current_group(request)

	groups =[]
	for group in Group.objects.all().order_by('title'):
		groups.append({
			'id': group.id,
			'title': group.title,
			'leader': group.leader and (u'%s %s' % (
				group.leader.first_name, 
				group.leader.last_name)) or None,
			'selected': cur_group and cur_group.id ==group.id and True or False
			})

	return groups


def get_current_group(request):
	"""Returns currently selected group or None"""

	#we remember selected group in a cookie
	pk =request.COOKIES.get('current_group')

	if pk:
		from .models import Group
		try:
			group =Group.objects.get(pk =int(pk))
		except Group.DoesNotExist:
			return None
		else:
			return group
	else:
		return None


def get_lang(request):
  if request.COOKIES.get('django_language') == 'en':
     pk = u'English'
     return pk
  elif request.COOKIES.get('django_language') == 'uk':
     pk = u'Українська'
     return pk
  elif request.COOKIES.get('django_language') == 'ru':
     pk = u'Русский'
     return pk
  #if we dont selected language - get LANGUAGE_CODE from settings
  #LANGUAGE_CODE сontains value of language in user browser
  else:
  	 if LANGUAGE_CODE == 'uk':
  	 	pk = u'Українська'
  	 elif LANGUAGE_CODE == 'ru':
  	 	pk = u'Русский'
  	 elif LANGUAGE_CODE == 'en':
  	 	pk = u'English'
  	 #if user browser use another lang - we write 'select' 
  	 else:
  	 	pk = u'select'
  	 return pk


def get_style(request):
  if request.COOKIES.get('current_style') == 'default':
     pk = '#d9edf7'
     return pk
  elif request.COOKIES.get('current_style') == 'gold':
     pk = '#f0ad4e'
     return pk
  elif request.COOKIES.get('current_style') == 'brown':
     pk = '#943126'
     return pk
  elif request.COOKIES.get('current_style') == 'grey':
     pk = '#af9090'
     return pk
  elif request.COOKIES.get('current_style') == 'black':
     pk = '#272822'
     return pk
  elif request.COOKIES.get('current_style') == 'blue':
     pk = '#0275d8'
     return pk
  elif request.COOKIES.get('current_style') == 'blue-w':
     pk = '#5bc0de'
     return pk
  elif request.COOKIES.get('current_style') == 'green':
     pk = '#5cb85c'
     return pk
  elif request.COOKIES.get('current_style') == 'rose':
     pk = '#f9ebea'
     return pk
  elif request.COOKIES.get('current_style') == 'sand':
     pk = '#f9e79f'
     return pk
  elif request.COOKIES.get('current_style') == 'night':
     pk = '#043b68'
     return pk
  elif request.COOKIES.get('current_style') == 'navy':
     pk = '#226f75'
     return pk
  #if we dont selected style - blue #d9edf7 will be default
  else:
  	 pk = '#d9edf7'
  	 return pk


def get_background(request):
  if request.COOKIES.get('current_bg') == 'white':
     pk = '#FFFAFA'
     return pk
  elif request.COOKIES.get('current_bg') == 'black':
     pk = '#272822'
     return pk
  elif request.COOKIES.get('current_bg') == 'grey':
     pk = '#616a6b'
     return pk
  elif request.COOKIES.get('current_bg') == 'rose':
     pk = '#fcf3cf'
     return pk
  elif request.COOKIES.get('current_bg') == 'bronze':
     pk = '#7f554f'
     return pk
  elif request.COOKIES.get('current_bg') == 'sand':
     pk = '#f9e79f'
     return pk
  elif request.COOKIES.get('current_bg') == 'blue':
     pk = '#d9edf7'
     return pk
  elif request.COOKIES.get('current_bg') == 'military':
     pk = '#d1d88c'
     return pk
  #if we dont selected background - white #FFFAFA will be default
  else:
  	 pk = '#FFFAFA'
  	 return pk


def get_color_text(request):
  if request.COOKIES.get('current_tc') == 'white':
     pk = '#ffffff'
     return pk
  elif request.COOKIES.get('current_tc') == 'black':
     pk = '#333'
     return pk
  elif request.COOKIES.get('current_tc') == 'grey':
     pk = '#cccccc'
     return pk
  elif request.COOKIES.get('current_tc') == 'orange':
     pk = '#ef5a04'
     return pk
  elif request.COOKIES.get('current_tc') == 'green':
     pk = '#5cb85c'
     return pk
  elif request.COOKIES.get('current_tc') == 'sand':
     pk = '#f9e79f'
     return pk
  elif request.COOKIES.get('current_tc') == 'blue':
     pk = '#5bc0de'
     return pk
  #if we dont selected color - black #333 will be default
  else:
  	 pk = '#333'
  	 return pk


def set_link(request):
  if request.COOKIES.get('current_bg') == 'white':
     link = '#428bca'
     return link
  elif request.COOKIES.get('current_bg') == 'black':
     link = '#5bc0de'
     return link
  elif request.COOKIES.get('current_bg') == 'grey':
     link = '#5bc0de'
     return link
  elif request.COOKIES.get('current_bg') == 'rose':
     link = '#428bca'
     return link
  elif request.COOKIES.get('current_bg') == 'bronze':
     link = '#5bc0de'
     return link
  elif request.COOKIES.get('current_bg') == 'sand':
     link = '#154360'
     return link
  elif request.COOKIES.get('current_bg') == 'blue':
     link = '#154360'
     return link
  elif request.COOKIES.get('current_bg') == 'military':
     link = '#154360'
     return link
  #if we dont selected background - white #FFFAFA will be default
  else:
  	 link = '#428bca'
  	 return link


def set_focus(request):
  if request.COOKIES.get('current_bg') == 'white':
     focus = '#2a6496'
     return focus
  elif request.COOKIES.get('current_bg') == 'black':
     focus = 'white'
     return focus
  elif request.COOKIES.get('current_bg') == 'grey':
     focus = 'white'
     return focus
  elif request.COOKIES.get('current_bg') == 'rose':
     focus = '#2a6496'
     return focus
  elif request.COOKIES.get('current_bg') == 'bronze':
     focus = 'white'
     return focus
  elif request.COOKIES.get('current_bg') == 'sand':
     focus = '#2a6496'
     return focus
  elif request.COOKIES.get('current_bg') == 'blue':
     focus = '#2a6496'
     return focus
  elif request.COOKIES.get('current_bg') == 'military':
     focus = '#2a6496'
     return focus
  #if we dont selected background - white #FFFAFA will be default
  else:
  	 focus = '#2a6496'
  	 return focus
 
 
	