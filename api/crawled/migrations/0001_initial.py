# Generated by Django 5.0.7 on 2024-07-16 08:17

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('additional_data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Entities',
                'db_table': 'entities',
                'db_table_comment': 'Entities owning domains.',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'db_table': 'tags',
                'db_table_comment': 'Classification tags for domains and webpages.',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=2000, unique=True)),
                ('favicon_base64', models.TextField(blank=True, db_index=True, null=True)),
                ('server', models.CharField(blank=True, max_length=100, null=True)),
                ('last_crawl_date', models.IntegerField(default=0)),
                ('number_of_crawls', models.IntegerField(default=0)),
                ('number_of_successful_crawls', models.IntegerField(default=0)),
                ('average_crawl_time', models.IntegerField(default=0)),
                ('domain_rank', models.FloatField(blank=True, null=True)),
                ('site_structure', models.JSONField(blank=True, null=True)),
                ('created', models.IntegerField(blank=True, null=True)),
                ('parent_entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crawled.entity')),
                ('tags', models.ManyToManyField(to='crawled.tag')),
            ],
            options={
                'db_table': 'domains',
                'db_table_comment': 'Found Tor domains. Domain has many Webpages.',
            },
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_index=True, max_length=2000, unique=True)),
                ('is_homepage', models.BooleanField(default=False)),
                ('url_after_request', models.URLField(max_length=2000)),
                ('last_request_date', models.IntegerField(default=0)),
                ('last_successful_request_date', models.IntegerField(default=0)),
                ('last_http_status', models.CharField(blank=True, max_length=3, null=True)),
                ('last_http_status_logs', models.JSONField(blank=True, null=True)),
                ('average_response_time', models.FloatField(default=0)),
                ('number_of_requests', models.IntegerField(default=0)),
                ('number_of_successful_requests', models.IntegerField(default=0)),
                ('page_rank', models.FloatField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('linking_to_webpages_logs', models.JSONField(blank=True, null=True)),
                ('anchor_texts', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2000), blank=True, null=True, size=None)),
                ('translated_anchor_texts', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2000), blank=True, null=True, size=None)),
                ('created', models.IntegerField(blank=True, null=True)),
                ('linking_to_webpages', models.ManyToManyField(related_name='_linking_from_webpages', to='crawled.webpage')),
                ('parent_domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawled.domain')),
                ('tags', models.ManyToManyField(to='crawled.tag')),
            ],
            options={
                'db_table': 'webpages',
                'db_table_comment': 'Webpages found while crawling a Tor domain.',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_text', models.TextField(blank=True, null=True)),
                ('detected_language', models.CharField(blank=True, max_length=100, null=True)),
                ('translated_text', models.TextField(blank=True, null=True)),
                ('page_title', models.CharField(blank=True, db_index=True, max_length=2000, null=True)),
                ('meta_title', models.CharField(blank=True, db_index=True, max_length=2000, null=True)),
                ('meta_description', models.TextField(blank=True, db_index=True, null=True)),
                ('on_page_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=2000), blank=True, null=True, size=None)),
                ('on_page_processed_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=2000), blank=True, null=True, size=None)),
                ('webpage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crawled.webpage')),
            ],
            options={
                'verbose_name_plural': 'Data',
                'db_table': 'data',
                'db_table_comment': 'Webpage data saved while crawling.',
            },
        ),
        migrations.AddConstraint(
            model_name='webpage',
            constraint=models.UniqueConstraint(condition=models.Q(('is_homepage', True)), fields=('is_homepage',), name='There can be only one homepage.'),
        ),
    ]
