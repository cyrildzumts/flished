from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from core import renderers
from jasiri import utils

import logging
import re
import json






NAME_PATTERN = re.compile(r"[,.-_\\]")

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def core_trans(value):
    if isinstance(value, str):
        return _(value)
    return value

@register.filter
def access_dict(_dict, key):
    if isinstance(_dict, dict) :
        return _dict.get(key, None)
    return None


@register.simple_tag
@register.filter
def replace_newline(value):
    if not isinstance(value, str):
        return value
    
    return value.replace("\\n","<br />\\n")

@register.simple_tag
@register.filter
def render_post(post):
    if not isinstance(post, dict):
        return post
    
    return renderers.render_post(post)



@register.simple_tag
@register.filter
def splitize(value):
    if not isinstance(value, str):
        return value
    result = " ".join(NAME_PATTERN.split(value))
    return result

@register.simple_tag(takes_context=True)
def json_ld(context, structured_data):
    request = context['request']
    structured_data['url'] = request.build_absolute_uri()
    indent = '\n'
    dumped = json.dumps(structured_data, ensure_ascii=False, indent=True, sort_keys=True)
    script_tag = f"\n<script type=\"application/ld+json\">{indent}{dumped}{indent}</script>"
    return mark_safe(script_tag)


def render_post(blocks):
    pass


