from rest_framework import serializers

from .models import Book, Author, Review

class ReviewModSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('book', )
        
        
class BookModSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)
    author = serializers.CharField(source='author.first_name')
    #reviews = ReviewModSerializer(many=True, read_only=True)
    review = serializers.StringRelatedField(many=True, read_only=True, source='reviews')
    class Meta:
        model = Book
        fields = ['id','title', 'author_id', 'author', 'avg_rating', 'number_ratings', 'review']
        
 

class AuthorModSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    book = serializers.StringRelatedField(many=True, read_only=True, source='books')
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'address','name', 'book']
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
        
    def validate(self, data):
        if len(data['first_name']) == 0 or len(data['last_name']) == 0:
            raise serializers.ValidationError("Please enter Author name.")
        elif Author.objects.filter(first_name=data['first_name'].title(),last_name=data['last_name'].title()).exists():
            raise serializers.ValidationError("Author already exists")
        else:
            return data        
        
    # field level validation
    # def validate_first_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short.")
    #     else:
    #         return value
        




    
