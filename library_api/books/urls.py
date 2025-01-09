# Import necessary modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, BookViewSet, MemberViewSet, BorrowTransactionViewSet,
    BorrowBookView, ReturnBookView, OverdueBooksView, AdminReportView, ExportReportView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import login_view  # Adjust the import according to your view

# Define the router for API views
router = DefaultRouter()
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')
router.register('members', MemberViewSet, basename='member')
router.register('transactions', BorrowTransactionViewSet, basename='transaction')

# Define URL patterns
urlpatterns = [
    # Web-based routes
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('books/', views.book_list, name='book_list'),
    path('borrowing-history/', views.borrowing_history, name='borrowing_history'),
    path('login/', login_view, name='login'),

    



    # API routes
    path('api/', include(router.urls)),
    path('api/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('api/return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path('api/overdue-books/', OverdueBooksView.as_view(), name='overdue-books'),
    path('api/admin-report/', AdminReportView.as_view(), name='admin-report'),
    path('api/export-report/', ExportReportView.as_view(), name='export-report'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
