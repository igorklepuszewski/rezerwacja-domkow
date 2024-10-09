from datetime import timedelta
from django import forms
import django_filters
from domki.models import House
from django.db.models import Q

class HouseFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter("start_date", label='Początek rezerwacji', widget=forms.DateInput(attrs={'type': 'date'}), method="filter_start_date")
    # end_date = django_filters.DateFilter("end_date", label='Koniec rezerwacji', widget=forms.DateInput(attrs={'type': 'date'}), method="filter_start_date")

    start_date = django_filters.DateFilter("start_date", label='Początek rezerwacji', widget=forms.DateInput(attrs={'type': 'date'}), method="filter_date_range")
    end_date = django_filters.DateFilter("end_date", label='Koniec rezerwacji', widget=forms.DateInput(attrs={'type': 'date'}), method="filter_date_range")
    class Meta:
        model = House
        fields = {
            'name': ['icontains'],  # nazwa domku ma zawierac
        }

    def filter_date_range(self, queryset, field_name, value):
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')

        if start_date and end_date:
            # Clean the input dates
            start_date = forms.DateField().clean(start_date)
            end_date = forms.DateField().clean(end_date)
            
            # Get the overlapping reservations filter
            overlapping_reservations_filter = House.get_selected_days_reserved_filter(start_date, end_date)
            queryset = queryset.exclude(overlapping_reservations_filter)
            
        return queryset
    # def filter_start_date(self, queryset, field_name, value):
    #    # chcemy domki, ktore sa wolne od start_date do start_date+1
    #    if value != "":
    #     end_date = value+timedelta(days=1)
    #     free_house_filter = ~House.get_selected_days_reserved_filter(value, end_date)
    #     queryset = queryset.filter(free_house_filter)
    #    return queryset
    
    # def filter_end_date(self, queryset, field_name, value):
    #    if value != "":
    #     start_date = value-timedelta(days=1)
    #     free_house_filter = ~House.get_selected_days_reserved_filter(start_date, value)
    #     queryset = queryset.filter(free_house_filter)
    #    return queryset