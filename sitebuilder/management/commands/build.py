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
    # 设置中的区域设置在执行命令时报错, False时会强制设置为'en-US'
    leave_locale_alone = True
    
    # < 1.8, 管理命令基于`optparse`, 位置参数传给`*args`, 可选给`**options`
    # >= 1.8, 基于`argparse`, 默认参数都给`**options`
    # 命名位置参数为`args`(兼容模式), 不推荐
    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')
    
    def handle(self, *args, **options):
        """ Request pages and build output. """
        # python prototypes.py build        # build == file name
        # python prototypes.py build index  # compile a single page
        # cd _build
        # python -m http.server 9000        # run simple python server
        
        settings.DEBUG = False
        settings.COMPRESS_ENABLED = True
        
        # 参数存在, 可为多个
        if args:
            pages = args
            available = list(get_pages())
            invalid = []
            for page in pages:
                if page not in available:
                    invalid.append(page)
                if invalid:
                    msg = 'Invalid pages: {}'.format(', '.join(invalid))
                    # 如果没有任何名字存在, 报错
                    raise CommandError(msg)
        else:
            pages = get_pages()
            # 如果存在文件夹, 删除
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
            os.makedirs(settings.STATIC_ROOT)
        
        # 调用`collectstatic`命令收集static文件
        call_command('collectstatic', interactive=False, clear=True, verbosity=0)
        call_command('compress', interactive=False, force=True)     # 压缩静态文件
        
        client = Client()
        # 遍历pages, 收集所有html
        for page in pages:
            url = reverse('page', kwargs={'slug': page})
            # 利用Django的test client, 模拟爬取网页
            response = client.get(url)
            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                # 文件夹不存在再创建
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                # 写入已经渲染好的静态网页
                f.write(response.content)
