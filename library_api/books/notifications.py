from django.core.mail import send_mail
from datetime import timedelta, date
from .models import Borrow

def send_overdue_notifications():
    overdue_borrows = Borrow.objects.filter(is_returned=False)
    for borrow in overdue_borrows:
        if borrow.borrowed_date + timedelta(days=14) < date.today():
            subject = "Overdue Book Notification"
            message = f"Dear {borrow.user.username},\n\n" \
                      f"The book '{borrow.book.title}' you borrowed is overdue. Please return it as soon as possible."
            recipient_list = [borrow.user.email]
            send_mail(subject, message, 'your_email@gmail.com', recipient_list)
