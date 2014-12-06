from django.contrib import admin
from core.models import *

admin.autodiscover()

admin.site.register(Article)
admin.site.register(Color)

admin.site.register(Recommended)

admin.site.register(ArticleType)
admin.site.register(ArticleSubType)
