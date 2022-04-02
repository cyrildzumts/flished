from django.template.loader import render_to_string

import logging
logger = logging.getLogger(__name__)
SUMMARY_TAG = "paragraph"
IMAGE_TAG = "image"

def render_table(table, template_name="editor/table.html"):
    return render_to_string(template_name, {'table': table})

def render_list(list_tool, template_name="editor/list.html"):
    return render_to_string(template_name, {'list': list_tool})


def render_header(head, template_name="editor/head.html"):
    return render_to_string(template_name, {'head': head})

def render_checklist(checklist, template_name="editor/checklist.html"):
    return render_to_string(template_name, {'checklist:': checklist})

def render_paragraph(paragraph, template_name="editor/paragraph.html"):
    return render_to_string(template_name, {'paragraph': paragraph})

def render_quote(quote, template_name="editor/quote.html"):
    return render_to_string(template_name, {'quote': quote})

def render_linktool(linktool, template_name="editor/linktool.html"):
    return render_to_string(template_name, {'linktool': linktool})


def render_image(image, template_name="editor/image.html"):
    return render_to_string(template_name, {'image': image})


BLOCK_MAPPING = {
    'header': render_header,
    'paragraph': render_paragraph,
    'table': render_table,
    'list': render_list,
    'linkTool': render_linktool,
    'checklist': render_checklist,
    'quote': render_quote,
    'image': render_image,
}