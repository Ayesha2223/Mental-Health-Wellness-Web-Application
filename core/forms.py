from django import forms
from django.contrib.auth.models import User
from .models import MoodEntry
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'gratitude']
        widgets = {
            'mood': forms.Select(choices=[
                ('Happy', '😊 Happy'),
                ('Sad', '😢 Sad'),
                ('Anxious', '😟 Anxious'),
                ('Calm', '😌 Calm'),
                ('Excited', '🤩 Excited'),
                ('Tired', '😴 Tired'),
            ], attrs={'class': 'form-select'}),
            'gratitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'I’m grateful for...'}),
        }



from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']


from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    """Form for updating additional profile fields"""
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ['bio']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})