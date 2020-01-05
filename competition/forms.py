from django import forms


class UploadForm(forms.Form):
    uploaded_file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
    )


class RegisterationForm(forms.Form):
    #manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    student_card_image = forms.ImageField()
    university = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class participantForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    student_card_image = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
