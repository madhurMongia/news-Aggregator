from scrapy_djangoitem import DjangoItem
from api.models import TechPost,EconomyPost,SportsPost,MarketPost

class TechNewsItem(DjangoItem):
    django_model = TechPost
    
class EconomynewsItem(DjangoItem):
    django_model = EconomyPost
    
class SportsNewsItem(DjangoItem):
    django_model = SportsPost

class MarketNewsItem(DjangoItem):
    django_model = MarketPost