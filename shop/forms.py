from django import forms
from .models import Customer
from django.contrib.auth import authenticate

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'confirm-password'}),
        required=True
    )
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'register-email-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'register-email-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'register-email-2'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'register-email-2'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register-password-2'}),
        }


    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken. Please choose a different one.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if Customer.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        return username
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password doesnot match.')
        return password

    




class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.PasswordInput({"type":"password", "class":"form-control", "id":"register-password-2", "name":"password"}),
        required=True
                               )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")

        return cleaned_data