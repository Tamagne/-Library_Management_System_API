from django.core.management.base import BaseCommand
from books.notifications import send_overdue_notifications

class Command(BaseCommand):
    help = "Send overdue notifications to users"

    def handle(self, *args, **kwargs):
        send_overdue_notifications()
        self.stdout.write("Overdue notifications sent successfully.")
