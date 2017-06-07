"""
May or may not be used
"""
from django import forms

from PepBandWebsite.models import Song, Meme


class addSong(forms.ModelForm):
    """
    Adds a song to the database
    """
    title = forms.CharField(required=True)
    public = forms.BooleanField(required=True)

    class Meta:
        model = Song
        fields = ("title", "public")

    def save(self, commit=True):
        entry = Song()
        entry.title = self.cleaned_data['title']
        entry.public = self.cleaned_data['public']

        if commit:
            entry.save()
        return entry


class changeSong(forms.ModelForm):
    """
    Changes the fields for a song
    """
    title = forms.CharField(required=True)
    public = forms.BooleanField(required=True)

    class Meta:
        model = Song
        fields = ('title', 'public')

    def save(self, commit=True, instance=None):
        entry = Song()
        entry.title = self.cleaned_data['title']
        entry.public = self.cleaned_data['public']

        if commit:
            entry.save()

        return entry

class addMeme(forms.ModelForm):
    """
    Adds a meme to the database
    """
    name = forms.CharField(required=True)

    class Meta:
        model = Song
        fields = ("name")

    def save(self, commit=True):
        entry = Meme()
        entry.name = self.cleaned_data['title']

        if commit:
            entry.save()
        return entry