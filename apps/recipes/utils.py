from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.conf import settings
import os

def fetch_pdf_resources(uri, rel):
    # if uri.find(settings.MEDIA_URL) != -1:
    #     path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    # breakpoint()
    if uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.STATIC_URL, ''))
        # TODO: dirty hack!
        print(path)
    else:
        path = None
    print('PATH:', path)
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=fetch_pdf_resources)
    print('render_2_pdf')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
