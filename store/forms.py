from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'sentiment_score']
        #fields = ['subject', 'review', 'rating', 'sentiment_score']
        widgets = {
            'sentiment_score': forms.HiddenInput()
        }
