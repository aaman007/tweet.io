import math

from rest_framework import status
from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size = 10
    min_page_size = 10
    max_page_size = 50
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data, **kwargs):
        page_size = int(self.request.query_params.get('page_size', self.page_size))
        if page_size < self.min_page_size or page_size > self.max_page_size:
            return Response(
                {'error': f'page_size must be between {self.min_page_size} and {self.max_page_size}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'count': self.page.paginator.count,
            'pages': math.ceil(self.page.paginator.count / page_size),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data,
        }, status=status.HTTP_200_OK)
