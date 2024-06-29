"""
Test cases for AsyncSpider class.
"""
from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError, Response
from logic.spiders.asynchronous import AsyncSpider


@pytest.fixture
def spider(example_url_object):
    """Fixture returning an instance of AsyncSpider class."""
    spider = AsyncSpider(
        initial_url=example_url_object,
        proxy='http://test:8118',
        user_agent='Mozilla/Test',
        max_requests=5,
        sleep_time=1,
    )
    return spider


class TestAsyncSpider:
    """Test cases for AsyncSpider class."""

    @patch('logic.spiders.asynchronous.httpx.AsyncClient.get')
    @pytest.mark.asyncio
    async def test_async_spider_get_method_returns_response_and_url_object(
        self,
        mock_get,
        spider,
        example_text_response,
        example_url_object,
    ):
        """
        Test that AsyncSpider get method is returning tuple with Response and Url objects.
        """
        mock_respone = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_respone, example_url_object

        response = await spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

