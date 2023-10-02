from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

# class Mypagination(PageNumberPagination):
#     page_size = 3
#     # page_query_param='num'
#     page_size_query_param='data'


# class Mypagination(LimitOffsetPagination):
#     default_limit=5
#     limit_query_param='datalimit'
#     offset_query_param='offsetlimit'

class Mypagination(CursorPagination):
    page_size = 3
    ordering = 'id'
    # cursor_query_param='pn'