from django import forms


class SearchForm(forms.Form):
    keywords = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'search-bar',
                                                                       'placeholder': 'Enter keywords or name of paper'}))
