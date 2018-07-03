# -*- coding: utf-8 -*-

from django import template

register = template.Library()


# Usage: {% pagenav object_list=students is_paginated=is_paginated
# paganator=paginator %}

@register.inclusion_tag('students/pagination.html')
def pagenav(object_list, is_paginated, paginator):
    return {
        'object_list': object_list,
        'is_paginated': is_paginated,
        'paginator': paginator
    }

