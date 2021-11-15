from parser.app import app
import pytest
from flask import Flask


class TestViews:

    def test_home_page(self):
        with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.status_code == 200
            assert b"Parse Articles" in response.data
            assert b"Show Articles" in response.data

    def test_articles_page(self):
        with app.test_client() as test_client:
            response = test_client.get('/articles_list')
            assert response.status_code == 200
            assert b"Category" in response.data

    def test_statistics_page(self):
        with app.test_client() as test_client:
            response = test_client.get('/statistics')
            assert response.status_code == 200
            assert b"Database sources statistics" in response.data
            assert b"Sport files statistics" in response.data

    @pytest.mark.empty
    def test_empty_articles_page(self):
        with app.test_client() as test_client:
            response = test_client.get('/articles_list')
            assert response.status_code == 200
            assert b"Politics" not in response.data

    @pytest.mark.empty
    def test_empty_statistics_page(self):
        with app.test_client() as test_client:
            response = test_client.get('/statistics')
            assert response.status_code == 200
            assert b"There is no records in database" in response.data
