from django.test import TestCase
from books.models import Author, Book, Member, BorrowTransaction, Borrow
from django.contrib.auth.models import User


class AuthorModelTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(name="J.K. Rowling", biography="Famous author of Harry Potter.")
        self.assertEqual(author.name, "J.K. Rowling")
        self.assertEqual(author.biography, "Famous author of Harry Potter.")

class BookModelTest(TestCase):
    def test_create_book(self):
        author = Author.objects.create(name="George Orwell", biography="Author of 1984.")
        book = Book.objects.create(
            title="1984",
            author=author,
            isbn="1234567890123",
            publication_date="1949-06-08"
        )
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author.name, "George Orwell")



class BorrowReturnTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(title="Test Book", author="Test Author", publication_date="2020-01-01", genre="Fiction")
    
    def test_borrow_book(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post('/borrow/', {"book": self.book.id})
        self.assertEqual(response.status_code, 201)
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_borrowed)
    
    def test_return_book(self):
        borrow = Borrow.objects.create(user=self.user, book=self.book)
        self.client.login(username="testuser", password="password")
        response = self.client.put(f'/return/{borrow.id}/', {"is_returned": True})
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_borrowed)

def test_overdue_books(self):
    borrow = Borrow.objects.create(user=self.user, book=self.book, borrowed_date="2020-01-01")
    self.client.login(username="testuser", password="password")
    response = self.client.get('/overdue-books/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data[0]["is_overdue"])

def test_admin_report(self):
    self.client.login(username="admin", password="adminpassword")
    response = self.client.get('/admin-report/')
    self.assertEqual(response.status_code, 200)
    self.assertIn("total_books", response.data)
    self.assertIn("total_borrowed", response.data)
