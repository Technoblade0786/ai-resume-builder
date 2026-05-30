from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ResumeInputForm(forms.Form):
    TEMPLATE_CHOICES = [
        ("modern", "Modern"),
        ("simple", "Simple"),
        ("ats", "ATS Friendly"),
    ]

    full_name = forms.CharField(max_length=100)
    job_title = forms.CharField(max_length=100)

    skills = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(widget=forms.Textarea, required=False)
    projects = forms.CharField(widget=forms.Textarea, required=False)

    template = forms.ChoiceField(
        choices=TEMPLATE_CHOICES,
        initial="modern",
        label="Resume Template"
    )

    use_ai = forms.BooleanField(required=False, label="Use AI Enhancement")

    openai_api_key = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="Your OpenAI API Key"
    )
