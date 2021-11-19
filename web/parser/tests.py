from parser.app import app
from parser.config import db
import pytest
from flask import Flask
from parser.models import Source
import re


class TestArticlesView:
    """Tests articles view."""

    @pytest.mark.empty
    def test_empty_articles_page(self):
        with app.test_client() as test_client:
            response = test_client.get("/")
            assert response.status_code == 200
            assert b"Politics" not in response.data

    def test_home_page(self):
        with app.test_client() as test_client:
            response = test_client.get("/")
            assert response.status_code == 200
            assert b"Parse Articles" in response.data
            assert b"Refresh News" in response.data

    def test_articles_page(self):
        with app.test_client() as test_client:
            response = test_client.get("/")
            assert response.status_code == 200
            assert b"Category" in response.data


class TestStatisticsViews:
    """Tests statistics view."""

    def test_statistics_page(self):
        with app.test_client() as test_client:
            response = test_client.get("/statistics")
            assert response.status_code == 200
            assert b"Database sources statistics" in response.data
            assert b"Sport files statistics" in response.data


class TestAddNewsViews:
    """Tests adding news source."""

    def test_get_add_news_page(self):
        with app.test_client() as test_client:
            response = test_client.get("/add_news")
            assert response.status_code == 200
            assert b"Name of source" in response.data
            assert b"Link to RSS feed" in response.data
            assert b"Link to source" in response.data
            assert b"Category" in response.data

    def test_post_add_news_page(self):
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as test_client:
            response = test_client.post("/add_news", data={'name': 'News', 'url': 'https://www.google.com/',
                                                           'source_link': 'https://www.google.com/',
                                                           'category': 'health'}, )
            assert response.status_code == 200
            source = db.session.query(Source).filter(Source.name == 'News').first()
            assert source != None
            db.session.delete(source)
            db.session.commit()
