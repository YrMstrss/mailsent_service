from django import forms

from client.models import Client
from mail.models import Newsletter, NewsletterSettings


class NewsletterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewsletterForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['clients'].queryset = Client.objects.filter(clients=user)
            self.fields['message'].queryset = NewsletterSettings.objects.filter(owner=user)

    class Meta:
        model = NewsletterSettings
        fields = ('clients', 'message', 'start_time', 'finish_time', 'period', 'status')
