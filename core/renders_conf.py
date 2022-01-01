from django.template.loader import render_to_string

import logging
logger = logging.getLogger(__name__)

def render_table(table, template_name="editor/table.html"):
    return render_to_string(template_name, table)

def render_list(list_tool, template_name="editor/list.html"):
    return render_to_string(template_name, list_tool)


def render_header(head, template_name="editor/head.html"):
    logger.info(f"rendering header : {head}")
    header = render_to_string(template_name, head)
    logger.info(f"rendering header string: {header}")
    return header

def render_checklist(checklist, template_name="editor/checklist.html"):
    return render_to_string(template_name, checklist)

def render_paragraph(paragraph, template_name="editor/paragraph.html"):
    logger.info(f"rendering paragraph : {paragraph}")
    return render_to_string(template_name, paragraph)

def render_quote(quote, template_name="editor/quote.html"):
    return render_to_string(template_name, quote)

def render_linktool(linktool, template_name="editor/linktool.html"):
    return render_to_string(template_name, linktool)


BLOCK_MAPPING = {
    'header': render_header,
    'paragraph': render_paragraph,
    'table': render_table,
    'list': render_list,
    'linkTool': render_linktool,
    'checklist': render_checklist,
    'quote': render_quote
}