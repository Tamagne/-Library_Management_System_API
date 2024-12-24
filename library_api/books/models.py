from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)  # Add this if missing

    def __str__(self):
        return self.name
    


class Book(models.Model):
    # Existing fields
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    genre = models.CharField(max_length=255)
    
    is_borrowed = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title




class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class BorrowTransaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow_transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_transactions')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Not Returned')

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"
    



class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="borrows")
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
    reservation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # "Borrowed", "Returned", etc.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

