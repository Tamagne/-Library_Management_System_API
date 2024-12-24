from rest_framework import serializers
from .models import Author, Book, Member, Borrow, BorrowTransaction
from rest_framework import serializers
from .models import BorrowTransaction  # Adjust according to your models

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction  # Replace with your actual model
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'date_of_birth', 'bio']



class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'isbn', 'genre', 'copies_available', 'publish_date']

    
        model = Borrow
        fields = ['id', 'user', 'book', 'borrowed_date', 'return_date', 'is_returned']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'membership_date', 'active_status']

class BorrowTransactionSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), source='member', write_only=True
    )
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = BorrowTransaction
        fields = ['id', 'member', 'member_id', 'book', 'book_id', 'borrow_date', 'return_date', 'status']


