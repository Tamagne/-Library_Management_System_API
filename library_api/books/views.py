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



from django.db import transaction

class CheckOutBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            with transaction.atomic():
                book = Book.objects.get(id=book_id)
                if book.available_copies > 0:
                    Transaction.objects.create(
                        user=request.user,
                        book=book,
                        check_out_date=timezone.now()
                    )
                    book.available_copies -= 1
                    book.save()
                    return Response({"message": "Book checked out successfully!"}, status=200)
                else:
                    return Response({"error": "No copies available!"}, status=400)
        except Book.DoesNotExist:
            return Response({"error": "Book not found!"}, status=404)

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            with transaction.atomic():
                book = Book.objects.get(id=book_id)
                transaction = Transaction.objects.filter(
                    user=request.user, 
                    book=book, 
                    return_date__isnull=True
                ).first()

                if not transaction:
                    return Response({"error": "No active borrow record found!"}, status=400)

                transaction.return_date = timezone.now()
                transaction.save()

                book.available_copies += 1
                book.save()
                return Response({"message": "Book returned successfully!"}, status=200)
        except Book.DoesNotExist:
            return Response({"error": "Book not found!"}, status=404)
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'published_date']
    search_fields = ['title', 'author__first_name']
    ordering_fields = ['published_date', 'title']

from django.shortcuts import get_object_or_404

class BookViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'books/home.html')

def about(request):
    return render(request, 'books/about.html')

def register(request):
    # Add registration logic here
    return render(request, 'books/register.html')

@login_required
def profile(request):
    return render(request, 'books/profile.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def login_view(request):
    return render(request, 'login.html')  # Adjust as needed

def logout_view(request):
    logout(request)
    return redirect('home')

from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

from django.shortcuts import render
from .models import BorrowingHistory

def borrowing_history(request):
    history = BorrowingHistory.objects.filter(user=request.user)
    return render(request, 'books/borrowing_history.html', {'history': history})

from django.http import JsonResponse

def api_home(request):
    return JsonResponse({'message': 'Welcome to the API!'})

