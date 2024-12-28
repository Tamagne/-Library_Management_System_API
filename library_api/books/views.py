from django.shortcuts import render
from rest_framework.views import APIView

from reportlab.pdfgen import canvas
from django.http import HttpResponse

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
from django.db.models import Count

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
    


class OverdueBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        overdue_books = Borrow.objects.filter(user=request.user, is_returned=False)
        overdue_books = [borrow for borrow in overdue_books if borrow.is_overdue()]
        overdue_data = [
            {"book": borrow.book.title, "borrowed_date": borrow.borrowed_date, "is_overdue": borrow.is_overdue()}
            for borrow in overdue_books
        ]
        return Response(overdue_data)
    


class AdminReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only admins can view this report."}, status=403)
        
        total_books = Book.objects.count()
        total_borrowed = Book.objects.filter(is_borrowed=True).count()
        most_borrowed_books = Borrow.objects.values('book__title').annotate(count=Count('book')).order_by('-count')[:5]

        report = {
            "total_books": total_books,
            "total_borrowed": total_borrowed,
            "most_borrowed_books": most_borrowed_books,
        }
        return Response(report)



class ExportReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only admins can export reports."}, status=403)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="library_report.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)

        # Write report data
        total_books = Book.objects.count()
        total_borrowed = Book.objects.filter(is_borrowed=True).count()
        p.drawString(100, 750, f"Total Books: {total_books}")
        p.drawString(100, 730, f"Total Borrowed: {total_borrowed}")

        # Example: List top 5 most borrowed books
        y_position = 700
        p.drawString(100, y_position, "Most Borrowed Books:")
        y_position -= 20
        most_borrowed_books = Borrow.objects.values('book__title').annotate(count=Count('book')).order_by('-count')[:5]
        for book in most_borrowed_books:
            p.drawString(100, y_position, f"{book['book__title']} - {book['count']} times")
            y_position -= 20

        p.showPage()
        p.save()
        return response
