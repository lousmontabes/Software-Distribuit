from django import forms
from .models import Reservation, Pick, Review, ComparatorData

class PickerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PickerForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "I want to eat "
        self.fields['city'].label = " in "

    class Meta:
        model = Pick
        fields = ["category", "city"]

class ReservationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['num_people'].label = "Number of people"

    class Meta:
        model = Reservation
        fields = ["day", "time_slot", "num_people"]

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["message", "rating"]

class ComparatorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ComparatorForm, self).__init__(*args, **kwargs)
        self.fields['price_average'].label = "Maximum price"

    class Meta:
        model = ComparatorData
        fields = ["city", "category", "price_average"]
