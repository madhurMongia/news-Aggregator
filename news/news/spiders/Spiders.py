from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import TechNewsItem,EconomynewsItem,SportsNewsItem,MarketNewsItem
import json
class TechCrunchSpider(Spider):
    name = 'techCrunch'
    def start_requests(self):
       cls = self.__class__
       for i in range(1,5):
        yield Request(f'https://techcrunch.com/wp-json/tc/v1/magazine?page={i}&_embed=true&cachePrevention=0', callback=self.parse_link)
       
    def parse_link(self,response):
        responses = json.loads(response.body)
        for res in responses:
            yield Request(res['link'],callback=self.parse_post,cb_kwargs= {'date' : res['date']})
            
    def parse_post(self,response, **kwargs): 
        headline = response.css('.article__title::text').get()
        story = response.css('.article-content p *::text').getall()
        container = TechNewsItem(headline = headline)
        container['story'] = self.to_str(story)
        container['summary'] = story[0]
        container['date_created'] = kwargs['date'][0:10]
        container['source'] = response.url
        yield container

    def to_str(self,list):
        story = ""
        for line in list:
            story += line
        return story
###################################################################
class EcoSpider(Spider):
    name = "economicsTimes"
    count = 0
    dates = {
        'Jan' : 1,'Feb' : 2,'Mar' : 3,'Apr' : 4,'May' : 5,'Jun' : 6,'Jul' : 7,'Aug' : 8,'Sep' : 9,'Oct' : 10,'Nov' : 11,'Dec' : 12
    }
    def start_requests(self):
        yield Request("https://economictimes.indiatimes.com/news/economy/articlelist/1286551815.cms",callback= self.parse_links)
        for i in range(3,8):
           yield Request(f"https://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=1286551815&curpg={i}&img=1",callback=self.parse_links)
        
    
    def parse_links(self,response):
        post_links = response.css('.eachStory h3 a::attr(href)').getall()
        print(post_links)
        for url in set(post_links):
            yield Request(f"https://economictimes.indiatimes.com/{url}",callback = self.parse_post,dont_filter= True)
    
    def parse_post(self,response):
        headline = response.css('.artTitle::text').get()
        story = response.css('.artText *::text').getall()
        date = response.css('time::text').get()
        container = EconomynewsItem(headline = headline)
        container['summary'] = self.get_summary(story)[:-1]
        container['story'] = ''.join(self.clear_story(story))
        container['date_created'] = f'{date[22:26]}-{self.dates.get(date[14:17])}-{date[18:20]}'
        container['source'] = response.url
        yield container
    def get_summary(self,story):
        summary = ""
        i = 0
        while story[i] != '\n':
            summary += story[i]
            i+=1
        return summary
    def clear_story(self,story):
        newStory = ""
        for line in story:
            newStory += line.replace("\n" ,"")
        return newStory
###################################################################
class SportSpider(Spider):
    
        name = "parimatch"
        
        def start_requests(self):
            yield Request("https://parimatchnews.com/",callback = self.parse_link)
            
        def parse_link(self,response):
            url_links = response.css('.post__item_link::attr(href)').getall()
            for url in url_links:
                yield Request(url,callback = self.parse_post)
        def parse_post(self,response):
            headline = response.css('.single-post__title::text').get()
            story = response.css('.single-post__content *::text').getall()
            container = SportsNewsItem()
            container['headline'] = self.clear(headline)
            container['summary'] = self.get_summary(self.clear(story))
            container['story'] = ''.join(self.clear(story))
            container['date_created'] = None
            container['source'] = response.url
            yield container
        def get_summary(self,story):
            summary = ""
            i = 0
            while(story[i] != '.'):
                summary += story[i]
                i+=1
            return summary
                
        def clear(self,story):
            newStory = ""
            for line in story:
                newStory += line.replace("\n" ,"")
            return newStory
###################################################################
class MarketSpider(Spider):
    name = 'equity'
    dates = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12,
    }
    def start_requests(self):
        for page in range(1,3):
            yield Request(f'https://www.moneycontrol.com/news/business/stocks/page-{page}/',callback = self.parse_link)
        
    def parse_link(self,response):
        url_posts = response.css('h2 a::attr(href)').getall()
        url_posts.pop(0)
        for url in url_posts:
            photos = False
            if url[34:40] == 'photos': photos = True
            yield Request(url,callback = self.parse_post,cb_kwargs = {'photos' : photos})
            
    def parse_post(self,response,**kwargs):
        headline = response.css('.article_title::text').get()
        story = response.css('#page1 .arti-flow p *::text').getall() if not kwargs['photos'] else response.css('.article_text::text').getall()
        summary = response.css('.article_desc::text').get()
        date = response.css('.article_schedule span::text').get()
        container = MarketNewsItem(headline = headline)
        container['story'] =''.join(story)
        container['summary'] = summary
        container['date_created'] =  f'{date[13:17]}-{self.dates.get(date[0:8])}-{date[9:11]}'
        container['source'] = response.url
        yield container