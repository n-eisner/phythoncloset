# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',
        'core.views.index'),

    (r'^landing$',
        'core.views.shopify_landing'),
    (r'^post-login$',
        'core.views.shopify_landing'),

    (r'^closet/$',
        'core.views.closet'),
    (r'^closet/add_file$',
        'core.views.closet_add_file'),

    (r'^outfit/$',
        'core.views.outfit'),
    (r'^outfit/p/(?P<slug>[a-zA-Z0-9=]+)$',
        'core.views.outfit_public'),

    (r'^scrape_url$',
        'core.views.scrape_shopping_url'),
    (r'^get_colors$',
        'core.views.get_colors_url'),

    (r'^about',
        'django.views.generic.simple.direct_to_template',
        {'template': 'general/about.html'}),
    (r'^help',
        'django.views.generic.simple.direct_to_template',
        {'template': 'general/help.html'}),
    (r'^policy',
        'django.views.generic.simple.direct_to_template',
        {'template': 'general/policy.html'}),
    (r'^terms',
        'django.views.generic.simple.direct_to_template',
        {'template': 'general/terms.html'}),

    (r'^settings/$',
        'core.views.user_settings'),
    (r'^settings/password_change/$',
        'django.contrib.auth.views.password_change',
        {'template_name': 'users/password_change_form.html'}),
    (r'^settings/password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'users/password_change_done.html'}),

    (r'^login$',
        'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'}),
    (r'^logout$',
        'django.contrib.auth.views.logout'),

    (r'^login/forgot/$',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'users/password_reset_form.html',
        'email_template_name': 'users/password_reset_email.html'}),
    (r'^login/forgot/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'users/password_reset_done.html'}),
    (r'^login/forgot/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'users/password_reset_confirm.html'}),
    (r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'users/password_reset_complete.html'}),

    (r'^admin/',
        include(admin.site.urls)),
    (r'^status/memcache/$',
        'core.management.memcached_status.view'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
