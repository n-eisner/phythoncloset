from django.db import models
from django.contrib.auth.models import User

from colorz import hsvToRGB, triplet

class ArticleType(models.Model):
    name = models.TextField()

    class Meta:
        verbose_name = ('ArticleType')
        verbose_name_plural = ('ArticleTypes')

    def __unicode__(self):
        return unicode(self.name)


class ArticleSubType(models.Model):
    name = models.TextField()
    article_type = models.ForeignKey(ArticleType)

    class Meta:
        verbose_name = ('ArticleSubType')
        verbose_name_plural = ('ArticleSubTypes')

    def __unicode__(self):
        return unicode(self.name)


class Color(models.Model):
    h = models.FloatField()
    s = models.FloatField()
    v = models.FloatField()

    class Meta:
        verbose_name = ('Color')
        verbose_name_plural = ('Colors')

    def __unicode__(self):
        return unicode(self.h) + ' ' + unicode(self.s) + ' ' + unicode(self.v)

    def hex(self):
        return triplet([int(x * 255) for x in hsvToRGB(self.h, self.s, self.v)])
    

class Article(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, blank=True)
    source_url = models.URLField(blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    image_url = models.URLField()

    article_sub_type = models.ForeignKey(ArticleSubType)

    class Meta:
        verbose_name = ('Article')
        verbose_name_plural = ('Articles')

    def __unicode__(self):
        return unicode(self.title)


class Recommended(models.Model):
    name = models.TextField()
    image_url = models.URLField()
    url = models.URLField()
    rec_for = models.ForeignKey(Article)
    article_type = models.ForeignKey(ArticleType)

    class Meta:
        verbose_name = ('Recommended')
        verbose_name_plural = ('Recommendeds')

    def __unicode__(self):
        return unicode(self.name) + ' for ' + unicode(self.rec_for)
