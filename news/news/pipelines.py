from itemadapter import ItemAdapter
from django.utils.text import slugify

class NewsPipeline:
    def process_item(self, item, spider):
        item['slug'] = slugify(item.get('headline'),allow_unicode=True)
        item.save()
        return item
