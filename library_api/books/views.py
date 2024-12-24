from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Author, Book, Member, BorrowTransaction
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowTransactionSerializer

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Borrow, Book
from .serializers import BorrowSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class BorrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__name']
    filterset_fields = ['is_borrowed']






class BorrowBookView(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.is_borrowed:
            raise serializers.ValidationError("This book is already borrowed.")
        book.is_borrowed = True
        book.save()
        serializer.save(user=self.request.user)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_returned:
            return Response({"error": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)
        instance.is_returned = True
        instance.return_date = timezone.now()
        instance.book.is_borrowed = False
        instance.book.save()
        instance.save()
        return Response({"message": "Book returned successfully."})
