from datetime import date
from django.test import TestCase

from domki.filters import HouseFilter
from domki.models import House, Reservation
from management.models import User


class TestHouseListViewFilters(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.house = House.objects.create(name="test_house")
        cls.user = User.objects.create_user(username='test_user', password='12345')

    def test_houses(self):
        start_date = date(2020, 4, 13)
        end_date = date(2020, 4, 15)
        res1 = Reservation.objects.create(house=self.house, user=self.user, start_date=start_date, end_date=end_date)
        is_reserved = self.house.is_selected_days_reserved(start_date, end_date)
        self.assertEqual(is_reserved, True)

    def test_house_free_between_two_reservation(self):
        # Create first reservation from 13 April to 15 April
        Reservation.objects.create(house=self.house, user=self.user, start_date=date(2020, 4, 13), end_date=date(2020, 4, 15))

        # Create second reservation from 28 April to 30 April
        Reservation.objects.create(house=self.house, user=self.user, start_date=date(2020, 4, 28), end_date=date(2020, 4, 30))

        # Now check for availability between 17 April and 26 April (which should be free)
        start_date = date(2020, 4, 17)
        end_date = date(2020, 4, 26)

        # Ensure the house is free between these dates
        self.assertEqual(self.house.is_selected_days_reserved(start_date, end_date), False)

        # Apply the filter
        house_filter = HouseFilter(data={'start_date': start_date, 'end_date': end_date})
        filtered_houses = house_filter.qs

        # Check that the house appears in the filtered results
        self.assertIn(self.house, filtered_houses)

    def test_filter(self):
        house_filter = HouseFilter()
        self.assertEqual(house_filter.qs.count(),1)

    

        