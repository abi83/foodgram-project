import os
from io import BytesIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def fetch_pdf_resources(uri, rel):
    """
    Convert path to css styles to pdf render
    """
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        try:
            path = os.path.join(
                settings.STATIC_ROOT,
                uri.replace(settings.STATIC_URL, ''))
        except TypeError:
            # no STATIC_ROOT in local_settings
            path = os.path.join(
                settings.BASE_DIR,
                uri.replace(settings.STATIC_URL, 'staticfiles/'))
    else:
        path = None
    return path


def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),
                            result,
                            encoding='UTF-8',
                            link_callback=fetch_pdf_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_first_user_id():
    """
    Depricated method was used for SET_DEFAULT author to recipes.
    It is here for migrations compability
    """
    User = get_user_model()
    return User.objects.filter(is_superuser=True)[0].pk
