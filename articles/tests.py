import pytest
from django.test import TestCase, Client
from .models import Article

class ArticlesTestCase(TestCase):
    def setUp(self):
        Article.objects.all().delete()
        self.articles = [
            Article.objects.create(slug='some-article-shortname', format='news', title="Заголовок первый"),
            Article.objects.create(slug='other-shortname', format='news', title="Заголовок второй"),
            Article.objects.create(slug='yet-another-article', format='longread', title="Следующий заголовок"),
            Article.objects.create(slug='other-shortname', format='faq', title="Какая-то ерунда"),
        ]
        self.client = Client()

    def test_simple_select(self):
        """
            Базовая проверка, что отбираются указанные статьи
        """
        resp = self.client.get(
            "/api/v1/articles/?names=" + ','.join(f"{a.format}/{a.slug}" for a in self.articles[:3])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), {
            'status': 'ok',
            'data': [dict(a) for a in self.articles[:3]],
        })

    def test_no_names(self):
        """
            Без указания конкретных names получаем пустой список
        """
        resp = self.client.get(
            "/api/v1/articles/"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), {'status': 'ok', 'data': []})

    def test_select_order(self):
        """
            Проверяем сохранение последовательности запрошенных элементов
        """
        resp = self.client.get(
            "/api/v1/articles/?names=" + ','.join(f"{a.format}/{a.slug}" for a in self.articles[2::-1])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), {
            'status': 'ok',
            'data': [dict(a) for a in self.articles[2::-1]],
        })

    def test_wrong_name(self):
        """
            Проверяем валидацию параметров
        """
        for msg, names, code in [
            ("Wrong article format", "joke/some-article-shortname,news/other-shortname", 400),
            ("Extra spaces", "news/some-article-shortname ,news/other-shortname", 400),
            ("Unexisting article slug", "news/hip-hop,news/other-shortname", 404),
        ]:
            resp = self.client.get(f"/api/v1/articles/?names={names}")
            self.assertEqual(resp.status_code, code, msg)

    def test_wrong_method(self):
        """
            Проверяем реакцию на не GET методы
        """
        resp = self.client.post(
            "/api/v1/articles/?names=" + ','.join(f"{a.format}/{a.slug}" for a in self.articles[:3])
        )
        self.assertEqual(resp.status_code, 405)

