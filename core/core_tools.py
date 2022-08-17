import os
from unittest import result
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Count, Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext_lazy as _
from django.forms import modelform_factory
from django.forms import formset_factory, modelformset_factory
from django.utils.text import slugify
from blog.models import Category, Tag, Post, News
from flished import utils, settings
from xhtml2pdf import pisa
import logging
import datetime
import io
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
HTTP_OK = 200
HEADERS = {
    'User-Agent': USER_AGENT
}

def create_instance(model, data):
    Form = modelform_factory(model, fields=model.FORM_FIELDS)
    form = Form(data)
    if form.is_valid():
        return form.save()
    else:
        logger.warn(f"Error on creating a new instance of {model}")
        logger.error(form.errors)
    return None


def update_instance(model, instance, data):
    Form = modelform_factory(model, fields=model.FORM_FIELDS)
    form = Form(data, instance=instance)
    if form.is_valid():
        return form.save()
    else:
        logger.warn(f"Error on updating an instance of {model}")
        logger.error(form.errors)
    return None


def delete_instance(model, data):
    logger.warn(f"Delete instance of {model} with data : {data}")
    return model.objects.filter(**data).delete()

def delete_instances(model, id_list):
    logger.warn(f"Delete instances of {model} with id in : {id_list}")
    return model.objects.filter(id__in=id_list).delete()


def instances_active_toggle(model, id_list, toggle=True):
    logger.warn(f"Updating active status for  instances of {model} with id in : {id_list}. new active status : {toggle}")
    return model.objects.filter(id__in=id_list).exclude(is_active=toggle).update(is_active=toggle)


def instances_sale_toggle(model, id_list, toggle=True):
    logger.warn(f"Updating active status for  instances of {model} with id in : {id_list}. new active status : {toggle}")
    return model.objects.filter(id__in=id_list).exclude(sale=toggle).update(sale=toggle)


def core_send_mail(recipient_list, subject, message):
    send_mail(subject, message, recipient_list)


def send_account_creation_confirmation(user):
    pass

def send_passwd_reset_confirmation(user):
    pass

def send_order_confirmation(order):
    pass

def send_order_cancel(order):
    pass

def send_payment_confirmation(order):
    pass

def send_shipment_confirmation(order):
    pass

def send_refund_confirmation(order):
    pass



def generate_invoice(order, debug=False, output_name=None):
    template_name = "invoices/invoice.html"
    
    now = datetime.datetime.now()
    #start_date = now - datetime.timedelta(days=now.day-1, hours=now.hour, minutes=now.minute, seconds=now.second)
    #end_delta = datetime.timedelta(days=1,hours=-23, minutes=-59, seconds=-59)
    #end_date = datetime.datetime(now.year, now.month +1, 1) - end_delta
    #user_seller =  None


    
    context = {
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'DATE': now,
        'orientation' : 'portrait',
        'FRAME_NUMBER' : 2,
        'page_size': 'letter portrait',
        'border': debug,
        'TOTAL' : order.total,
        'COUNT': order.quantity,
        'CURRENCY': settings.CURRENCY,
        'INVOICE_TITLE' : f"Invoice-{order.order_ref_number}-{order.created_at}",
        'order': order
    }
    output_name = output_name or f"Invoice-{order.order_ref_number}-{order.created_at}.pdf"
    invoice_html = render_to_string(template_name, context)
    invoice_file = io.BytesIO()
    pdf_status = pisa.CreatePDF(invoice_html, dest=invoice_file, debug=False)
    if pdf_status.err:
        logger.error("error when creating the report pdf")
        return None
    else:
        logger.info("recharge report pdf created")
    return invoice_file







def save_file(byteio_file, filename):
    if not byteio_file or not filename:
        logger.warning("save_report : byteio_file or filename is missing")
        return
    with open(filename, 'w+b') as f :
        f.write(byteio_file.getbuffer())
    
def save_pdf_file(order, debug=True):
    byteio_file = generate_invoice(order, debug=debug)
    if not byteio_file:
        return
    output_name = f"Invoice-{order.order_ref_number}-{order.created_at}.pdf"
    with open(output_name, 'w+b') as f :
        f.write(byteio_file.getbuffer())



def slugify_categories():
    queryset = Category.objects.filter(slug=None)
    for c in queryset:
        c.slug = slugify(c.name)
        c.save()

    
def slugify_post():
    queryset = Post.objects.filter(slug=None)
    for p in queryset:
        p.slug = slugify(p.name)
        p.save()

def validate_structured_data(structured_data):
    pass

def generate_website_structure_data():
    sd = {
        "@content": settings.JSON_LD_CONTEXT,
        "@type": settings.JSON_LD_TYPE_WEBSITE,
        #'url': settings.SITE_HOST + "/fr/",
        "potentialAction": {
            "@type": settings.JSON_LD_TYPE_SEARCHACTION,
            "target": {
                "@type": settings.JSON_LD_TYPE_ENTRY_POINT,
                "urlTemplate": settings.SITE_HOST + "/fr/search/?search={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    }
    return sd




def generate_categories_translations():
    queryset = list(Category.objects.all())
    created_at = datetime.datetime.now().isoformat('-')
    filename = f"translation_tools/categories-{created_at}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    descriptions = []
    descriptions.append(f"# This file is generated automatically at {created_at}")
    descriptions.append(f"# Don't change this content unless you know what you are doing\n\n")
    descriptions.append("# CATEGORIES DESCRIPTION \n\n")
    for c in queryset:
        var = "CATEGORY_" + "_".join(str(c.name).upper().split('-')) + "_DESCRIPTION"
        descriptions.append(f"{var} = _(\"{c.description}\")")
    
    # build context strings
    s = ""
    f_string_template = f"\"{s}\" : {{\"description\": {s},\"meta-keywords\":\"\",\"page-title\":\"\"}},"
    contexts = []
    contexts.append("# CATEGORIES DESCRIPTION CONTEXTS\n\n")
    contexts.append(f"CATEGORY_DESCRIPTION_CONTEXT = {{")
    for c in queryset:
        description = "CATEGORY_" + "_".join(str(c.name).upper().split('-')) + "_DESCRIPTION"
        #contexts.append(f"\"{c.name}\": {description},")
        contexts.append(f"\"{c.name}\" : {{\"description\": {description}, \"meta-keywords\":\"\",\"page-title\":\"\"}},")
    contexts.append(f"}}")
    try:
        with open(filename, 'w',newline='\n') as f:
            for line in descriptions:
                f.write(line)
                f.write("\n")
            for line in contexts:
                f.write(line)
                f.write("\n")

        logger.info(f"Categories Descriptions translations generated : {filename}")
    except Exception as e:
        logger.warn(f"Error while creating {filename}")
        logger.exception(e)


def core_fetch_url(url):
    logger.info(f"Fetching Url : {url}")
    response = requests.get(url, timeout=60, headers=HEADERS)
    if response.status_code != HTTP_OK:
        logger.warning(f"Url {url} not found.")
        return {'success': 0, 'link': url, 'meta': {}}

    html_page = BeautifulSoup(response.content, "html.parser")
    meta_title = html_page.title.string,
    description_meta = html_page.find('meta', property="og:description", content=True)
    image_url =  html_page.find('meta', property="og:image")
    site_name =  html_page.find('meta', property="og:site_name")
    data = {
        "success": 1,
        "link": url,
        "meta": {
            "title": html_page.title.string,
            "description": description_meta.attrs.get('content'),
            "site_name": site_name.attrs.get("content"),
            "image":{
                "url": image_url.attrs.get('content')
            }
        }
    }
    return data