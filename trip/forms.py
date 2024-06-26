import datetime
from django.utils.translation import gettext_lazy as _
from django import forms


from images.forms import MultipleFileField
from tags.forms import AddTagForm
from trip.models import Trip


class AddTripForm(forms.ModelForm):
    image = MultipleFileField(label=_('image'), required=False)
    # slug = forms.CharField(required=False, widget=forms.HiddenInput())

    year = datetime.date.today().year
    date = forms.DateField(label=_('date'),
                           widget=forms.SelectDateWidget(years=tuple(range(year - 5, year + 3))))

    tag = AddTagForm
    # user = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Trip
        # exclude = ['slug', 'user']
        fields = [
            'title',

            'date',
            'title_photo',
            'content',
            'published',
            'category',
            'tag',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),

            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    # AIFormSet = forms.inlineformset_factory(Trip, Image, fields='__all__')
