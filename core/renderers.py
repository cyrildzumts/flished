from core.renders_conf import BLOCK_MAPPING, SUMMARY_TAG
from django.utils.safestring import mark_safe

def render_post(post_dict):
    html_blocks = [BLOCK_MAPPING[block.get('type')](block).replace("\n","<br />\n") for block in post_dict.get('blocks')]
    return mark_safe("".join(html_blocks))


def render_summary(post_dict):
    paragraph = None
    for block in post_dict.get('blocks'):
        if block.get('type') == SUMMARY_TAG:
            paragraph = block
            break
    if paragraph is not None:
        return mark_safe(BLOCK_MAPPING[paragraph.get('type')](paragraph).replace("\n","<br />\n"))
    return ""

    

