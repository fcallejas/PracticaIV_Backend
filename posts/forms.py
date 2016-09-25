from posts.models import Post
from django.forms import ModelForm, SelectDateWidget


class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['owner']
        widgets = {
            'publicate_at': SelectDateWidget()
        }
