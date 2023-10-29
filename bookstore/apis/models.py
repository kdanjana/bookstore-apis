from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    
    def __str__(self):
        return f'Author_id({self.id}):{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        self.address = self.address.title()        
        super(Author, self).save(*args, **kwargs)
    
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    avg_rating = models.FloatField(default=0)
    number_ratings = models.IntegerField(default=0)
        
    def __str__(self):
        return f'Book_id({self.id}):{self.title} written by {self.author} has avg_rating:{self.avg_rating}, ratings:{self.number_ratings}'
    

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=1000, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return f"Review_id({self.id}):Review of {self.book.title} by {self.reviewer.username}"
    