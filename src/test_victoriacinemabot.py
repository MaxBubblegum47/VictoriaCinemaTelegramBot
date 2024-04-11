
import pytest
from movie import Film
import os


class MockResponse:
    def __init__(self, content):
        self.content = content


def mock_get(url):
    if "https://www.victoriacinema.it/victoria_cinema/index.php" in url:
        with open("website.html", "rb") as f:
            return MockResponse(f.read())
    else:
        return MockResponse(b"")


@pytest.fixture
def mock_requests(monkeypatch):
    monkeypatch.setattr("requests.get", mock_get)


def test_web_scraping(mock_requests):
    Film.web_scraping()
    assert "website.html" in os.listdir()


def test_odd_movie(mock_requests):
    messageOdd = Film.Odd_Movie()
    assert isinstance(messageOdd, list)
    assert messageOdd


def test_even_movie(mock_requests):
    messageEven = Film.Even_Movie()
    assert isinstance(messageEven, list)
    assert messageEven
