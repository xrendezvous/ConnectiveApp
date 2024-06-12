from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Note
from django.core.exceptions import ValidationError


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Tag.objects.filter(name=name).exists():
            raise ValidationError("Тег з такою назвою вже існує.")
        return name


class NoteForm(ModelForm):
    title = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    body = CharField(
        min_length=10, max_length=150, required=True, widget=TextInput()
    )

    class Meta:
        model = Note
        fields = ["title", "body"]
        exclude = ["tag"]
