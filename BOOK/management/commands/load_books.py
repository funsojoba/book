from BOOK.models import Book

from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker()




class Command(BaseCommand):
    help = "Load books data"

    def handle(self, *args, **kwargs):
        TOTAL = 10

        for _ in range(TOTAL):
            Book.objects.create(
                title=fake.sentence(),
                author=fake.name(),
                description=fake.text(),
                price=fake.random_int(10, 100),
            )

        self.stdout.write(self.style.SUCCESS(f"{TOTAL} books created successfully"))