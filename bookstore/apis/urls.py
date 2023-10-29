from . import views
from django.urls import path

urlpatterns = [
    # to get list of all authors, to add an author to list
    path("authors/", views.AuthorsListView.as_view(), name='authors_list'),
    # to get/update/delete details of an author
    path("authors/<int:pk>", views.AuthorDetailView.as_view(), name='author_detail'),
    # to get list of all books, to add book to list
    path("books/", views.BooksListView.as_view(), name='books_list'),
    # to get/update/delete details of a book
    path("books/<int:pk>/", views.BookDetailView.as_view(), name='book_detail'),
    # get all reviews for a particular book
    path("books/<int:pk>/reviews/", views.BookReviewsView.as_view(), name='book_reviews'),
    # to write a review for a book
    path("books/<int:pk>/review_create/", views.BookReviewCreateView.as_view(), name='book_review_create'),
    # to get/update/delete a review
    path("books/review/<int:pk>/", views.ReviewDetailView.as_view(), name='review_detail'),
    # to get a list of all reviews
    path("reviews/", views.ReviewsListView.as_view(), name='reviews_list'),
    # to get a list of all reviews given by a user
    path("reviews/<str:username>/", views.UserReview.as_view(), name='users_review'),
   
    
    
    #path("authors", views.AuthorsView.as_view(), ),
    
]
