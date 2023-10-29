from rest_framework.pagination import PageNumberPagination

class BookListPagination(PageNumberPagination):
    page_size = 3
    #page_size_query_param = "size"
    #max_page_size = 4
    #last_page_strings = "end"
    