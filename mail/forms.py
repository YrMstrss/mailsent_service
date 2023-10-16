from django import forms

from mail.models import Newsletter, NewsletterSettings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('subject', 'body', 'mail_settings', 'clients')


class NewsletterSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = NewsletterSettings
        exclude = ('status', )
