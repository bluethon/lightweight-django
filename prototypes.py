#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-07-16 15:28
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

import os
import sys

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    SECRET_KEY='9adr8to-se-pw',
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        # 'django.contrib.webdesign',       # deprecated in 1.8, {% lorem %} built in
        'sitebuilder',
        'compressor',               # static file compress
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ),
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    SITE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),
    STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),
    # # 文件获得唯一hash(DEBUG=False生效)
    # STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage',
    # settings for django-compressor
    STATICFILES_FINDERS=(
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )
)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
