# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('core_tag')

        # Adding model 'Color'
        db.create_table('core_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('h', self.gf('django.db.models.fields.FloatField')()),
            ('s', self.gf('django.db.models.fields.FloatField')()),
            ('v', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['Color'])

        # Removing M2M table for field tags on 'Article'
        db.delete_table('core_article_tags')

        # Adding M2M table for field colors on 'Article'
        db.create_table('core_article_colors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['core.article'], null=False)),
            ('color', models.ForeignKey(orm['core.color'], null=False))
        ))
        db.create_unique('core_article_colors', ['article_id', 'color_id'])


    def backwards(self, orm):
        # Adding model 'Tag'
        db.create_table('core_tag', (
            ('tag', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Tag'])

        # Deleting model 'Color'
        db.delete_table('core_color')

        # Adding M2M table for field tags on 'Article'
        db.create_table('core_article_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['core.article'], null=False)),
            ('tag', models.ForeignKey(orm['core.tag'], null=False))
        ))
        db.create_unique('core_article_tags', ['article_id', 'tag_id'])

        # Removing M2M table for field colors on 'Article'
        db.delete_table('core_article_colors')


    models = {
        'core.article': {
            'Meta': {'object_name': 'Article'},
            'article_sub_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ArticleSubType']"}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Color']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'core.articlesubtype': {
            'Meta': {'object_name': 'ArticleSubType'},
            'article_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ArticleType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.articletype': {
            'Meta': {'object_name': 'ArticleType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.color': {
            'Meta': {'object_name': 'Color'},
            'h': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            's': ('django.db.models.fields.FloatField', [], {}),
            'v': ('django.db.models.fields.FloatField', [], {})
        },
        'core.recommended': {
            'Meta': {'object_name': 'Recommended'},
            'article_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ArticleType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'rec_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Article']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']