import pytest

from tests.utils import paginator_not_in_view_context, url_paginator_view

pytestmark = [pytest.mark.django_db]


class TestPaginatorView:
    url = '/'

    def test_index_paginator_not_in_view_context(self, client, few_posts_sale):
        paginator_not_in_view_context(
            client=client, data=few_posts_sale, url=self.url
        )

    def test_index_paginator_view(self, client, post_sale):
        url_paginator_view(client=client, data=post_sale, url=self.url)

    def test_review_paginator_not_in_view_context(self, client, few_review):
        url = f'/profile/{few_review.author.username}/reviews/'
        paginator_not_in_view_context(
            client=client, data=few_review, url=url
        )

    def test_review_paginator_view(self, client, review):
        url = f'/profile/{review.author.username}/reviews/'
        url_paginator_view(client=client, data=review, url=url)

    def test_profile_paginator_not_in_view_context(
            self, client, few_posts_sale):
        url = f'/profile/{few_posts_sale.author.username}/'
        paginator_not_in_view_context(
            client=client, data=few_posts_sale, url=url
        )

    def test_profile_paginator_view(self, client, post_sale):
        url = f'/profile/{post_sale.author.username}/'
        url_paginator_view(client=client, data=post_sale, url=url)
