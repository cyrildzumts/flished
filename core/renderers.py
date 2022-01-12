from core.renders_conf import BLOCK_MAPPING, SUMMARY_TAG
from django.utils.safestring import mark_safe
from django.template.defaultfilters import urlencode, escape

def render_post(post_dict):
    html_blocks = [BLOCK_MAPPING[block.get('type')](block) for block in post_dict.get('blocks')]
    return "".join(html_blocks)


def render_summary(post_dict):
    paragraph = None
    for block in post_dict.get('blocks'):
        if block.get('type') == SUMMARY_TAG:
            paragraph = block
            break
    if paragraph is not None:
        return mark_safe(BLOCK_MAPPING[paragraph.get('type')](paragraph))
    return ""

    

