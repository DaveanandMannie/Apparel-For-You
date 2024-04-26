from django.core.management.base import BaseCommand
from shop.models import ShoeSize


class Command(BaseCommand):
    help = 'Add shoe sizes to the database'

    def handle(self, *args, **options):
        start_size = 3.0
        end_size = 13.0
        step = 0.5

        current_size = start_size
        while current_size <= end_size:
            shoe_size = ShoeSize(size=current_size)
            shoe_size.save()
            current_size += step

        self.stdout.write(self.style.SUCCESS('Shoe sizes add successfully.'))
