import pytest


class TestCustomErrorPages:

    @pytest.mark.django_db(transaction=True)
    def test_custom_404(self, client):
        url_invalid = '/some_invalid_url_404/'
        code = 404
        response = client.get(url_invalid)
        assert response.status_code == code, (
            'Убедитесь, что для несуществующих адресов страниц, '
            f'сервер возвращает код {code}')
        try:
            from gael.urls import handler404
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон')

    @pytest.mark.django_db(transaction=True)
    def test_custom_500(self):
        code = 500
        try:
            from gael.urls import handler500
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон')

    @pytest.mark.django_db(transaction=True)
    def test_custom_403(self):
        code = 403
        try:
            from gael.urls import handler403
        except ImportError:
            assert False, (
                f'Убедитесь, что для страниц, возвращающих код {code}, '
                'настроен кастомный шаблон')
