from .util import get_groups
from .util import get_lang
from .util import get_style, get_color_text
from .util import get_background
from .util import set_link, set_focus

def groups_processor(request):
    return {'GROUPS': get_groups(request)}

#select language
def lang_processor(request):
	return {'PK': get_lang(request)}


#select style
def style_processor(request):
	return {'STYLE': get_style(request)}


#select background
def background_processor(request):
	return {'BACKGROUND': get_background(request)}


#select form-text
def color_text_processor(request):
	return {'TC': get_color_text(request)}


#select link color
def link_processor(request):
	return {'LINK': set_link(request)}


#select link focus color
def focus_processor(request):
	return {'FOCUS': set_focus(request)}





