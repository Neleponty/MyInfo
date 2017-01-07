#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import timezone
import time
import datetime
from grab import Grab
import re
from MyInfo.proj import SimpleModel


class ParserE1:
    header = None
    description = None
    source_url = None
    text = None
    images_urls = None

    def parse(self):
        g = Grab()
        g.go('www.e1.ru/news/')

        header = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Language': 'ru-RU',
            'Connection': 'Keep-Alive',
            'Host': 'www.e1.ru',
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'

        }

        g.setup(headers=header)

        response = g.response.unicode_body().encode('utf-8').decode('utf-8')

        # название
        pattern = 'class=\"big\"><strong>(.*?)</strong></a>'
        self.header = ''.join(re.findall(pattern, response))

        # описание
        pattern = 'text_all\">(.*?)</span>'
        self.description = ''.join(re.findall(pattern, response))

        # ссылка-источник новости
        pattern = 'href="(.*?)\" class=\"big\"'
        url = ''.join(re.findall(pattern, response))
        self.source_url = url[:int(len(url) / 2)]
        g.go(self.source_url)

        # текст
  #      f = open('openednews.txt', 'w')
        response = g.response.unicode_body().encode('utf-8').decode('utf-8')
        pattern = '<p>(.*?)</p>'
        self.text = ' '.join(re.findall(pattern, response))

        # ссылки на изображения
        pattern = 'link\"><a href=\"(.*?)\" '
        images_urls_array = re.findall(pattern, response)
        self.images_urls = ""
        for image in images_urls_array:
            self.images_urls += 'http://www.e1.ru'
            self.images_urls += image
            self.images_urls += '; '
#        f.write(response)
 #       f.close()

        return {'header': self.header,
                'description': self.description,
                'source_url': self.source_url,
                'text': self.text,
                'images_urls': self.images_urls}

    def start(self):
        parser = ParserE1()
        category = SimpleModel.Categories.objects.first()
        pause = 60
        print('parser e1 started. pause: ' + str(pause) + "sc")
        id = SimpleModel.News.objects.last().id

        while True:
            model = parser.parse()
            news = SimpleModel.News()
            news.header = model['header']
            news.content = model['text']
            #stupid
            news.category = category
            news.is_fav = 0
            news.likes = 0
            news.pub_date = timezone.now()
            news.id = id
            images_urls = [SimpleModel.PhotosUrls().setPath(id=id, path=image) for image in model['images_urls']]
            news.image = images_urls[0]
            photos = [SimpleModel.NewsPhotos().setPhoto(id=id, photo=photo, news=news) for photo in images_urls]
            oldnews = SimpleModel.News.objects.get(id=id-1)
            print(oldnews.header)
            if oldnews.header != news.header:
                news.save()
                [item.save() for item in images_urls]
                [item.save() for item in photos]
                id += 1

            time.sleep(pause)
