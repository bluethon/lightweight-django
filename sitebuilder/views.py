#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-07-16 15:30
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
# noinspection PyProtectedMember
from django.utils._os import safe_join


def get_page_or_404(name):
    """ Return page content as a Django template or raise 404 error. """
    try:
        # Use `safe_join`, return a normalized, absolute version of the final path
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page Not Found')

    with open(file_path, 'r') as f:
        # noinspection PyShadowingNames
        # instantiates Django template object
        page = Template(f.read())

    return page


def page(request, slug='index'):
    """ Render the requested page if found. """
    file_name = f'{slug}.html'
    # noinspection PyShadowingNames
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }
    return render(request, 'page.html', context)
