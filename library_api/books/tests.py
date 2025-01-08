from .models import Author, Book, User

class LibraryManagementTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a test author
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author",
        )

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,  # Use the Author instance here
            isbn="1234567890",
            published_date="2023-01-01",
            copies_available=5
        )
