from django.core.management.base import BaseCommand, CommandError
import random

from domki.models import House, Reservation
from management.models import User


from random import randrange
from datetime import date, timedelta, datetime


def random_date(start, end):
    """
    This function will return a random date between two date
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date = start + timedelta(seconds=random_second)
    return date(random_date.year, random_date.month, random_date.day)


def to_date(passed_date):
    return date(passed_date.year + 10, passed_date.month, passed_date.day)


class Command(BaseCommand):
    help = "Creates data for dev"

    def handle(self, *args, **options):
        user = User.objects.all().first()
        houses = list(House.objects.all())
        for _ in range(500):
            # losoujemy index domku
            index = random.randint(0, len(houses) - 1)
            house: House = houses[index]
            start_date = random_date(date(1990, 1, 1), to_date(datetime.now()))
            end_date = random_date(start_date, to_date(datetime.now()))
            if not house.is_selected_days_reserved(start_date, end_date):
                Reservation.objects.create(
                    user=user, house=houses[index], start_date=start_date, end_date=end_date
                )

        self.stdout.write(self.style.SUCCESS("REZERWACJE ZOSTALY STWORZONE"))
