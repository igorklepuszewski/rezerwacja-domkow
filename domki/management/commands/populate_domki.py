from django.core.management.base import BaseCommand, CommandError
import string
import random

from domki.models import House


class Command(BaseCommand):
    help = "Creates data for dev"

    def handle(self, *args, **options):
        for _ in range(100):
            name = ''.join(random.choices(string.ascii_letters, k=7))
            House.objects.create(name=name)


        self.stdout.write(
            self.style.SUCCESS('COMMAND HAS BEEN RUN')
        )