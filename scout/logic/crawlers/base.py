from logic.spiders.async_spider import AsyncSpider
from logic.parsers.url import URLExtractor
from typing import Iterator
import asyncio


class BaseCrawler:

    def __init__(self, found_urls=None):
        self.spider = AsyncSpider()
        self.url_extractor = URLExtractor
        # API Integration.
        self.client = None
        self.found_urls = found_urls if found_urls is not None else set()
        self.requested_urls = set()
        self.max_requests = 5
        self.sleep_time = 3

    async def crawl(self):
        """
        Basic crawl.
        Process here is really simple just look for urls and request them asynchronously.
        """
        # My manual implementation of limiting requests.
        lists_of_urls_list = self.ratelimit_urls(list(self.found_urls))

        for list_of_urls in lists_of_urls_list :
            responses = await self.spider.get_urls(iterator_of_urls=list_of_urls)
            await asyncio.sleep(self.sleep_time)

            for response in responses:

                # TODO:
                # Maybe good solution would be to implement API call here
                # Where I simply check if we have this url in DB already ?
                self.requested_urls.add(response['requested_url'])
                self.found_urls.remove(response['requested_url'])

                if response['status'] is not None:
                    # TODO:
                    # Update Webpage data with response
                    if response['raw_urls'] is not None:
                        processor = self.url_extractor(iterator_of_urls=response['raw_urls'], current_page_url=response['responsed_url'])
                        new_found_urls = await processor.process_found_urls()

                        # TODO:
                        # Create new urls in db right here.
                        self.found_urls.update(new_found_urls)
                        print(self.found_urls)
                        self.found_urls = self.found_urls.difference(self.requested_urls)
                        # Remove prints!

            if self.found_urls:
                # This will run for some time ;)
                await self.crawl()
            else:
                raise ValueError(f'last urls is empty: {self.found_urls}')

    async def crawl_single_domain(self):
        """
        Crawling process that just discovers all urls of specified domain.
        """
        pass

    async def fetch_urls(self):
        pass

    def filter_found_urls(self):
        pass

    def ratelimit_urls(self, urls):
        """
        My implementation of limiting number of requests send.
        Im simply spliting received iterator of urls to list of list with length of self.max_requests.
        Generate list of urls lists.
        """
        self.max_requests
        if len(urls) > self.max_requests:
            return [
                urls[x : x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]