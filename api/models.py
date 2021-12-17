from django.db import models

class TechPost(models.Model):
    headline= models.CharField(max_length = 500,blank = False)
    summary= models.TextField()
    story = models.TextField()
    date_created= models.DateField(null=True)
    slug = models.SlugField(primary_key=True ,unique=True,null=False)
    source = models.URLField()
    def __str__(self):
        return self.headline

class EconomyPost(models.Model):
    headline= models.CharField(max_length = 500,blank = False)
    summary= models.TextField()
    story = models.TextField()
    slug = models.SlugField(primary_key=True ,unique=True,null=False)
    date_created= models.DateField()
    source = models.URLField()
    def __str__(self):
        return self.headline

class SportsPost(models.Model):
    headline= models.CharField(max_length = 500,blank = False)
    summary= models.TextField()
    story = models.TextField()
    slug = models.SlugField(primary_key=True ,unique=True,null=False)
    date_created= models.DateField(null=True)
    source = models.URLField()
    def __str__(self):
        return self.headline

class MarketPost(models.Model):
    headline= models.CharField(max_length = 500,blank = False)
    summary= models.TextField()
    story = models.TextField()
    slug = models.SlugField(primary_key=True ,unique=True,null=False)
    date_created= models.DateField(null=True)
    source = models.URLField()
    def __str__(self):
        return self.headline
    
