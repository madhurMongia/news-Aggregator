import django
from celery import shared_task
import os
import sys
from django.conf import settings as django_settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
sys.path.append(os.path.join(django_settings.BASE_DIR, 'news'))
django.setup()
from news.spiders import Spiders
from news import settings
from crochet import setup

@shared_task
def scraping_periodic_task():
    setup()
    configure_logging()
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Spiders.TechSpider)
    process.start
    return Spiders.TechSpider
