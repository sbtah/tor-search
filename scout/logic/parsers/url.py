import re
from urllib.parse import urljoin, urlsplit
from lxml.html import HtmlElement
from utilities.logging import logger
from typing import List


class URLExtractor:

    def __init__(self, iterator_of_urls, current_page_url=None):
        self.iterator_of_urls = iterator_of_urls
        self.current_page_url = current_page_url
        self.logger = logger

    def get_domain(self, url) -> str:
        """
        Extracts domain from parsed URL.

        :arg url: String with URL address to extract domain from.
        """
        try:
            domain = urlsplit(url).netloc
            return domain
        except Exception as e:
            self.logger.error(f'(get_domain) Some other exception: {e}')
            raise

    def is_file(self, url):
        pass

    def clean_url(self, url: str) -> str:
        """
        Cleans URL of all query params or fragments.
        Returns cleaned URL.

        :arg url: String with URL address to clean.
        """
        try:
            result = urlsplit(url)
            if result.query or result.fragment:
                return urljoin(url, result.path)
            else:
                return url
        except Exception as e:
            self.logger.error(f'(clean_url) Some other Exception: {e}')
            raise

    def fix_paths(self, url: str) -> str:
        """
        Fixes path URL by joining it with domain.
        Returns proper URL on success.

        :arg url: String with URL address to fix.
        """
        try:
            if self.current_page_url is not None:
                fixed_url = urljoin(self.current_page_url, url)
                if self.is_valid_url(url=fixed_url):
                    return fixed_url
                else:
                    self.logger.info('Failed while fixing URL.')
                    return url
        except Exception as e:
            self.logger.error(f'(fix_paths) Some other Exception: {e}')
            raise

    def is_valid_url_parse(self, url: str) -> bool:
        """
        Validates URL by parsing it with urlsplit.

        :arg url: String with URL address to check.
        """
        try:
            result = urlsplit(url)
            return bool(result.scheme and result.netloc)
        except ValueError:
            return False

    def is_onion(self, url: str) -> bool:
        """
        Checks if given URL address is an onion URL.
        Returns bool.

        :arg url: String with URL address to check.
        """
        if url is not None:
            try:
                domain = urlsplit(url)
                if 'onion' in domain.netloc:
                    return True
                else:
                    return False
            except Exception as e:
                self.logger.error(f'(is_onion) Some other Exception: {e}')
                raise
        else:
            pass

    def is_valid_url_regex(self, url: str) -> bool:
        """
        Validates URL by Regex.

        :arg url: String with URL address to check.
        """
        try:
            pattern = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return bool(pattern.match(url))
        except Exception as e:
            self.logger.error(f'(is_valid_url_regex) Some other Exception: {e}')
            raise

    def is_valid_url(self, url: str) -> bool:
        """
        Validates URL by parsing and Regex.
        Returns bool.

        :arg url: String with URL address to check.
        """
        if self.is_valid_url_parse(url) is True and self.is_valid_url_regex(url) is True:
            return True
        return False

    def process_found_urls(self) -> List[str]:
        """
        Processes found URLS in many ways.
        First of all this method is cleaning URL of any query parameters and fragments.
        Then it tries to fix any paths by joining found urls with requested url.
        Lastly it checks validity of found URL and is URL an onion.
        """
        processed_urls = []
        if self.iterator_of_urls:
            for url in self.iterator_of_urls:
                cleaned = self.clean_url(url=url.strip())
                if self.is_valid_url(url=cleaned) and self.is_onion(url=cleaned):
                    processed_urls.append(cleaned)
                else:
                    fixed = self.fix_paths(url=cleaned)
                    if self.is_onion(url=fixed) and self.is_valid_url(url=fixed):
                        processed_urls.append(fixed)
                    else:
                        pass
            return processed_urls