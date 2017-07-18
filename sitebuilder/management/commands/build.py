#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2017-07-17 15:43
# @Author   : Bluethon (j5088794@gmail.com)
# @Link     : http://github.com/bluethon

import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.test.client import Client


def get_pages():
    # 调用一次返回一个文件名
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]


class Command(BaseCommand):
    help = 'Build static site output.'
    
    def handle(self, *args, **options):
        """ Request pages and build output. """
        # python prototypes.py build        # build == file name
        # cd _build
        # python -m http.server 9000        # run simple python server

        if args:
            pages = args
            avaiable = list(get_pages())
            invalid = []
            for page in pages:
                if page not in avaiable:
                    


        # 如果存在文件夹, 删除
        if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
            shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)

        os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
        os.makedirs(settings.STATIC_ROOT)

        # 调用`collectstatic`命令收集static文件
        call_command('collectstatic', interactive=False, clear=True, verbosity=0)

        client = Client()
        # 遍历pages, 收集所有html
        for page in get_pages():
            url = reverse('page', kwargs={'slug': page})
            # 利用Django的test client, 模拟爬取网页
            response = client.get(url)
            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                os.makedirs(output_dir)
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                # 写入已经渲染好的静态网页
                f.write(response.content)
