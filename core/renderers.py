from core.renders_conf import BLOCK_MAPPING


def render_post(post_dict):
    html_blocks = [BLOCK_MAPPING[block.get('type')](block) for block in post_dict.get('blocks')]
    return "".join(html_blocks)

    

