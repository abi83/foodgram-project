from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.forms import EmailField

User = get_user_model()


class CreationForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'User with email {email} already exists')
        return email

    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )
