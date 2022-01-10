# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use
# pylint: disable=unused-argument
from parser.app import app
from parser.config import db
from parser.models import Source

import pytest


@pytest.fixture(scope='module')
def test_client():
    """Create a test client using the Flask application configured for testing."""
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


class TestBase:
    """Base test class."""
    url = ''
    data = ''
    HTTP_GET = 200
    HTTP_POST = 201

    @pytest.fixture()
    def get_response(self, test_client):
        """Simple get response test."""
        response = test_client.get(self.url)
        assert response.status_code == self.HTTP_GET
        return response

    @pytest.fixture()
    def post_response(self, test_client):
        """Simple post response test."""
        response = test_client.post(self.url, data=self.data)
        assert response.status_code == self.HTTP_POST
        return response



class TestArticlesView(TestBase):
    """Test articles view."""
    url = "/"

    @pytest.mark.empty
    def test_empty_articles_page(self, get_response):
        assert b"Politics" not in get_response.data

    def test_home_page(self, get_response):
        assert b"Parse Articles" in get_response.data
        assert b"Category" in get_response.data


class TestStatisticsViews(TestBase):
    """Test statistics view."""
    url = "/statistics"

    def test_statistics_page(self, get_response):
        assert b"Database sources statistics" in get_response.data
        assert b"Sport files statistics" in get_response.data


class TestAddNewsViews(TestBase):
    """Test adding news source."""
    url = "/add_news"
    data = {
        "name": "News",
        "url": "https://www.google.com/",
        "source_link": "https://www.google.com/",
        "category": "health",
    }

    def test_get_add_news_page(self, get_response):
        assert b"Name of source" in get_response.data
        assert b"Link to RSS feed" in get_response.data
        assert b"Link to source" in get_response.data
        assert b"Category" in get_response.data

    def test_post_add_news_page(self, post_response):
        source = db.session.query(Source).filter(Source.name == self.data["name"]).first()
        assert source is not None
        db.session.delete(source)
        db.session.commit()
