from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'perPage'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        no_pagination = request.query_params.get('noPagination', 'false').lower() == 'true'

        if no_pagination:
            self.page = None
            self.request = request
            return list(queryset)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if self.page is None:
            return Response({
                'total_items': len(data),
                'total_pages': 1,
                'current_page': 1,
                'perPage': len(data),
                'next': None,
                'previous': None,
                'results': data
            })

        next_page = None
        if self.page.has_next():
            next_page = self.get_next_link()

        previous_page = None
        if self.page.has_previous():
            previous_page = self.get_previous_link()

        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'perPage': self.page_size,
            'next': next_page,
            'previous': previous_page,
            'results': data
        })
