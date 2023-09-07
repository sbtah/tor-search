from django.db import models
from urllib.parse import urlsplit
import time
from django.contrib.postgres.fields import ArrayField


class Tag(models.Model):

    value = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.value


class Website(models.Model):
    """Class for Website objects."""

    domain = models.URLField(max_length=255, unique=True)
    title = models.CharField(max_length=2000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    last_crawl = models.IntegerField(blank=True, null=True)
    # website_map = models.JSONField(blank=True, null=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    description_tags = models.ManyToManyField(Tag)
    site_structure = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.domain


class Webpage(models.Model):
    """Class for Webpage objects."""

    parent_website = models.ForeignKey(Website, on_delete=models.CASCADE)

    url = models.URLField(max_length=2000, unique=True)
    # Since we could get redirected.
    url_after_request = models.URLField(max_length=2000)
    last_http_status = models.CharField(max_length=3, blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=2000, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    # We will skip files from crawling.
    is_file = models.BooleanField(default=False)
    last_visit = models.IntegerField(blank=True, null=True)
    on_page_onion_urls = ArrayField(models.URLField(max_length=2000), null=True, blank=True)

    # How many times we successfully requested this url?
    number_of_successful_requests = models.IntegerField(blank=True, null=True)
    number_of_unsuccessful_requests = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    number_of_references = models.IntegerField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)


    def __str__(self):
        return self.url
