'''
This test checks 3 things:
- if the website works
- the scraping functionality
- if the odd messages and the even messages are available
'''
import pytest
from movie import Film
import os


class MockResponse:
    def __init__(self, content):
        self.content = content

# Check the response of the website to see if the website works properly
def mock_get(url):
    if "https://www.victoriacinema.it/victoria_cinema/index.php" in url:
        with open("website.html", "rb") as f:
            return MockResponse(f.read())
    else:
        return MockResponse(b"")


@pytest.fixture
def mock_requests(monkeypatch):
    monkeypatch.setattr("requests.get", mock_get)

# Check is website.html is available, if not, that means that the
# web_scraping method of the class Film, didn't work properly
def test_web_scraping(mock_requests):
    Film.web_scraping()
    assert "website.html" in os.listdir()

# Check if the messageOdd is correclty generated, otherwise there is something wrong
def test_odd_movie(mock_requests):
    messageOdd = Film.Odd_Movie()
    assert isinstance(messageOdd, list)
    assert messageOdd

# Check if the messageEven is correclty generated, otherwise there is something wrong
def test_even_movie(mock_requests):
    messageEven = Film.Even_Movie()
    assert isinstance(messageEven, list)
    assert messageEven
