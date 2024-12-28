from django import forms
from django.contrib.auth.models import User
from users.models import Profile



class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control small-field", "placeholder": "Confirm Password"}),
        label="Confirm Password"
    )
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control  small-field", "placeholder": "User name"}),
            "first_name": forms.TextInput(attrs={"class": "form-control small-field fname", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control small-field lname", "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control small-field", "placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control small-field", "placeholder": "Password"}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class UserLoginForm(forms.ModelForm):
   
    class Meta:
        model=User
        fields=["username","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control ","placeholder":"User name"}),
            "password":forms.PasswordInput(attrs={"class":"form-control ","placeholder":"Password"})
        }
    


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'profile_picture'] 

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }  
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile



class InquiryForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    message = forms.CharField(widget=forms.Textarea, required=True)   




   