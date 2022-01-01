from core.renders_conf import BLOCK_MAPPING


def render_post(post_dict):
    html_blocks = [BLOCK_MAPPING[block.get('type')]().replace("\\n","<br />\\n") for block in post_dict.get('blocks')]
    return "".join(html_blocks)

    

