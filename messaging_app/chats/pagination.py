from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class NumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def _page_counter(self, data):
        return Response(
            {
                'count': self.page.paginator.count
            }
        )