from core.renders_conf import BLOCK_MAPPING
from django.utils.safestring import mark_safe

def render_post(post_dict):
    html_blocks = [BLOCK_MAPPING[block.get('type')](block).replace("\n","<br />\n") for block in post_dict.get('blocks')]
    return mark_safe("".join(html_blocks))

    

