from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from domki.filters import HouseFilter
from domki.forms import ReservationForm
from domki.models import House, Reservation
from django.views.decorators.csrf import csrf_protect

from django_filters.views import FilterView

# Create your views here.


# | OR
# & AND
# ~ NOT
class HouseListView(FilterView, ListView):
    model = House
    template_name = "house_list.html"
    filterset_class = HouseFilter
    

class HouseDetailView(DetailView):
    model = House
    template_name = "house_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationForm()
        return context

@csrf_protect
def create_reservation(request, pk):
    if request.method == "POST" and request.user.is_authenticated:
        form = ReservationForm(request.POST)
        house = get_object_or_404(House, pk=pk)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            if not house.is_selected_days_reserved(start_date, end_date):
                Reservation.objects.create(
                    house=house,
                    user=request.user,
                    start_date = start_date,
                    end_date=end_date,
                )
                return redirect('user-detail', request.user.id)
        else:
            return render(request, "house_detail.html", {"object": house, "form":form})
    return redirect("house-list")

