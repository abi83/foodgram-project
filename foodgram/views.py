import logging

from django.shortcuts import render
from django.views.generic.base import View

logger = logging.getLogger('foodgram')


class Handler404(View):
    @staticmethod
    def get(request, exception):  # noqa
        logger.warning("404: page not found at {}".format(request.path))
        return render(request, 'misc/404.html',
                      {'path': request.path}, status=404)


class Handler500(View):
    @staticmethod
    def dispatch(request, *args, **kwargs):
        logger.error("500: page is broken {}".format(request.path))
        return render(request, 'misc/500.html', status=500)


class About(View):
    @staticmethod
    def get(request):
        return render(request, 'about.html')


class Tech(View):
    @staticmethod
    def get(request):
        return render(request, 'tech.html')
