# coding: utf-8

import base64
import hashlib
import simplejson as json
import urlparse
import requests
from bs4 import BeautifulSoup
import colorsys

from django.conf import settings
from django.utils import simplejson
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q

from core.models import *
import colorz

def index(request):
    # if not request.user.is_authenticated():
    return render(request, 'index.html')

    data = {}

    return redirect('/closet')


# @login_required
def closet(request):
	data = {
		'current_tab': 'closet',
		'article_types': ArticleType.objects.all(),
		'article_sub_types': ArticleSubType.objects.all(),
	}

	if request.GET.get('type'):
		try:
			article_type = ArticleType.objects.get(id=request.GET.get('type'))
			article_sub_types = ArticleSubType.objects.filter(article_type=article_type)
			data['articles'] = Article.objects.filter(article_sub_type__in=article_sub_types).order_by('-id')
			data['selected_type'] = article_type
		except ValueError:
			pass

	if 'articles' not in data:
		data['articles'] = Article.objects.select_related('article_sub_type').prefetch_related('colors').order_by('-id')

	if 'q' in request.GET:
		data['articles'] = data['articles'].filter(Q(title__icontains=request.GET.get('q')) | Q(description__icontains=request.GET.get('q')))
		data['search_query'] = request.GET.get('q')

	return render(request, 'closet.html', data)


@login_required
def closet_add_file(request):
	data = {
		'current_tab': 'closet',
	}

	if not request.POST.get('image_url'):
		return redirect('/closet?error')

	colors = [colorz.hsvbucket(*colorz.rgb2hsv(*colorz.rgb(x.replace('#', '')))) for x in request.POST.get('image_colors', '').strip().split('|') if x]
	color_objs = []
	for color_tri in colors:
		color_obj, created = Color.objects.get_or_create(
				h=color_tri[0],
				s=color_tri[1],
				v=color_tri[2]
			)
		color_objs.append(color_obj)

	article_sub_type = ArticleSubType.objects.get(id=request.POST.get('clothing_type'))

	new_article = Article(
			title=request.POST.get('title'),
			image_url=request.POST.get('image_url'),
			description=request.POST.get('description'),
			article_sub_type=article_sub_type,
			user=request.user
		)

	new_article.save()
	new_article.colors.add(*color_objs)

	if 'next' in request.GET:
		return redirect(request.GET.get('next'))

	return redirect('/closet?new')


def get_weather():
	weather = cache.get('phl_weather')
	if not weather:
		URL = 'http://query.yahooapis.com/v1/public/yql?q=use "https://raw.github.com/yql/yql-tables/master/weather/weather.woeid.xml" as weather; select * from weather where w in (select place.woeid from flickr.places where lat=39.95400120000001 and lon=-75.1958487 and api_key=07518c5da6dcda6f2d8126ca45fbf085) and u="f";&format=json&env=http://datatables.org/alltables.env'
		weather = json.loads(requests.get(URL).text)['query']['results']['rss']['channel']
		cache.set('phl_weather', weather, 300)
	return weather


# @login_required
def outfit(request):
	data = {
		'current_tab': 'outfit',
		'hostname': settings.HOSTNAME,
		'outfit': {
			'heads': [],
			'tops': [],
			'bottoms': [],
			'feet': [],
		},
		'recommended':{
			'tops': None
		},
	}

	data['weather'] = get_weather()

	to_get_kinds = {
		'tops': [['Tops (Long Sleeve)'], ['Sweaters']],
		'bottoms': [['Pants']],
	}
	temp_current, temp_high, temp_low = int(data['weather']['item']['condition']['temp']), int(data['weather']['item']['forecast'][0]['high']), int(data['weather']['item']['forecast'][0]['low'])

	if (temp_current + temp_high + temp_low) / 3 > 80 or temp_high > 90:
		to_get_kinds = {
			'tops': [['Tops (Short Sleeve)']],
			'bottoms': [['Shorts', 'Skirts']]
		}
	elif (temp_current + temp_high + temp_low) / 3 > 60:
		to_get_kinds = {
			'tops': [['Tops (Long Sleeve)'], ['Sweaters']],
			'bottoms': [['Pants', 'Skirts']]
		}
	elif (temp_current + temp_high + temp_low) / 3 > 40:
		to_get_kinds = {
			'tops': [['Tops (Long Sleeve)'], ['Sweaters']],
			'bottoms': [['Pants']]
		}
	if (temp_current + temp_high + temp_low) / 3 < 40:
		to_get_kinds = {
			'tops': [['Tops (Long Sleeve)'], ['Sweaters'], ['Jackets']],
			'bottoms': [['Pants']],
		}

	data['to_get_kinds'] = to_get_kinds

	try:
		to_get = {}
		for kind in to_get_kinds:
			to_get[kind] = [ArticleSubType.objects.filter(article_type__name__in=x).all() for x in to_get_kinds[kind]]
			print to_get[kind], to_get_kinds[kind]

		for main_type in to_get:
			for sub_type in to_get[main_type]:
				try:
					data['outfit'][main_type].append(Article.objects.filter(article_sub_type__in=sub_type).order_by('?')[0])
				except IndexError:
					data['outfit'][main_type].append(None)
			try:
				data['recommended'][main_type] = Recommended.objects.filter(rec_for__in=data['outfit'][main_type]).order_by('?')[0]
			except IndexError:
				pass
	except IndexError:
		data['no_clothes'] = True
		raise

	data['encoded'] = base64.urlsafe_b64encode(json.dumps({x:[y.id if y is not None else None for y in data['outfit'][x]] for x in data['outfit']}))
	return render(request, 'outfit.html', data)


def outfit_public(request, slug):
	data = {
		'current_tab': 'outfit',
		'encoded': str(slug),
		'recommended': {},
		'hostname': settings.HOSTNAME,
		'public_link': True,
	}
	data['weather'] = get_weather()
	# TODO: add hash
	raw = json.loads(base64.urlsafe_b64decode(str(slug)))
	data['outfit'] = {x: [Article.objects.get(id=y) if y is not None else None for y in raw[x]] for x in raw}

	for main_type in data['outfit']:
		try:
			data['recommended'][main_type] = Recommended.objects.filter(rec_for__in=data['outfit'][main_type]).order_by('?')[0]
		except IndexError:
			pass
	return render(request, 'outfit.html', data)


# @login_required
def scrape_shopping_url(request):
	data = {
		'status': 'error'
	}

	if request.GET.get('url'):
		try:
			url_parts = urlparse.urlparse(request.GET.get('url'))
			if 'urbanoutfitters.com' in url_parts[1]:
				r = requests.get(request.GET.get('url'))
				soup = BeautifulSoup(r.text)

				data['image_url'] = soup.find(id="prodMainImg")['src']
				data['title'] = soup.find(id="prodTitle").string.strip()
				data['description'] = soup.find(id="detailsDescription").get_text().strip().strip('\n')
				data['status'] = 'ok'
			else:
				data['info'] = 'shop not supported'
		except Exception as e:
			print e

	return HttpResponse(simplejson.dumps(data), mimetype='application/json')


# @login_required
def get_colors_url(request):
	data = {
		'status': 'error'
	}

	if request.GET.get('url'):
		data['colors'] = cache.get('COLORZ_' + request.GET.get('url'))
		if not data['colors']:
			try:
				data['colors'] = colorz.get_colors_url(request.GET.get('url'))
				data['status'] = 'ok'
				cache.set('COLORZ_' + request.GET.get('url'), data['colors'], 8000)
			except Exception as e:
				print e
		else:
			data['status'] = 'ok'

	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def user_settings(request):
    data = {}

    return render(request, 'users/settings.html', data)


def shopify_landing(request):
	data = {
		'current_tab': 'closet',
		'article_sub_types': ArticleSubType.objects.all(),
	}

	token = request.GET.get('token')
	secret = 'd2de1b4091e84670ac2e568a45bd1bd2'

	the_hash = hashlib.sha256(token+secret).hexdigest()
	catalogs = requests.get('http://galileoplatform.shopyourway.com/catalogs/get-user-catalogs?token=%s&hash=%s' % (token, the_hash)).text
	data['catalogs'] = json.loads(requests.get('http://galileoplatform.shopyourway.com/catalogs/get?token=%s&hash=%s&ids=%s' % (token, the_hash, catalogs.strip('[]'))).text)

	all_items = []
	for catalog in data['catalogs']:
		all_items += [x['id'] for x in catalog['items']]

	all_the_items = json.loads(requests.get('http://galileoplatform.shopyourway.com/products/get?token=%s&hash=%s&ids=%s' % (token, the_hash, ','.join([str(x) for x in all_items]))).text)
	data['items'] = {x['id']: x for x in all_the_items}
	print data['items']

	return render(request, 'shopify_landing.html', data)


# def shopyourway_landing(request):
	# return redirect('/')