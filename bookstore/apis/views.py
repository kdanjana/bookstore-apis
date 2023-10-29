from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from .models import Author, Book, Review
from .serializers import AuthorModSerializer, BookModSerializer, ReviewModSerializer
from .permissions import ReviewUserOrReadOnly, AdminOrReadOnly
from .throttling import ReviewCreateThrottleRate, ReviewListThrottleRate
from .pagination import BookListPagination

# Create your views here.


class AuthorsListView(generics.ListCreateAPIView):
    """ to get list of all authors, to add an author to list"""
    throttle_classes = [AnonRateThrottle]
    permission_classes = [AdminOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorModSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']
    
    

    
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ to get/update details of an author, delete an author from list """
    permission_classes = [AdminOrReadOnly]
    serializer_class = AuthorModSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Author.objects.filter(id=pk)
       
    
      
class BooksListView(generics.ListCreateAPIView):
    """" to get list of all books, to add book to list   """
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    pagination_class = BookListPagination
    serializer_class = BookModSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author__first_name', 'reviews__rating']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """to get/update details of a book, delete book from list  """
    permission_classes = [AdminOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookModSerializer


 
class BookReviewsView(generics.ListAPIView):
    """ lists all  reviews of a book"""
    serializer_class = ReviewModSerializer
    throttle_classes = [UserRateThrottle]
    filter_backends = [filters.SearchFilter]
    search_fields = ['reviewer__username']
        
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(book=pk)
    
    

class BookReviewCreateView(generics.CreateAPIView):
    """ create a new review for a book"""
    permission_classes = [IsAuthenticated] # only logged in user can write a review
    serializer_class = ReviewModSerializer
    throttle_classes = [UserRateThrottle, ReviewCreateThrottleRate]  
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        book = Book.objects.get(pk=pk)
        current_user = self.request.user
        reqview_qs = Review.objects.filter(book=book, reviewer=current_user)
        if reqview_qs.exists():
            raise ValidationError("You have already given a review for this book.")
        if book.number_ratings == 0:
            book.avg_rating = serializer.validated_data['rating']
            book.number_ratings += 1
        else:  
            book.avg_rating = ((book.avg_rating*book.number_ratings)+ serializer.validated_data['rating']) / (book.number_ratings + 1)
            book.number_ratings += 1
        book.save()
        serializer.save(book=book, reviewer=current_user)
        
        


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ to get/ update a review, delete a review"""
    permission_classes = [ReviewUserOrReadOnly] # user who wrote review only can update/delete that review
    queryset = Review.objects.all()
    serializer_class = ReviewModSerializer
    throttle_classes = [UserRateThrottle]
     
    def perform_update(self, serializer):
        serializer.save()
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # get the review from the Review model
        instance = self.get_object()
        if 'rating' in  self.request.data:
            # get the book for which review is to be edited
            book = Book.objects.get(id=instance.book.id)
            new_rating = self.request.data['rating']
            old_rating = instance.rating
            book.avg_rating = (((book.avg_rating * book.number_ratings)- old_rating) + new_rating) / (book.number_ratings)
            book.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)      
        
    def perform_destroy(self, instance):
        book = Book.objects.get(id=instance.book.id)
        rating = instance.rating
        book.number_ratings -= 1
        book.avg_rating = ((book.avg_rating *(book.number_ratings + 1)) - rating) / (book.number_ratings)
        book.save()
        instance.delete()
    


class ReviewsListView(generics.ListAPIView):
    """ to get a list of all reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewModSerializer
    throttle_classes = [AnonRateThrottle, ReviewListThrottleRate]
 
    

class UserReview(generics.ListAPIView):
    """to get a list of all reviews given by a user """
    serializer_class = ReviewModSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(reviewer__username=username)
   