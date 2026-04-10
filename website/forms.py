from django import forms


class TenantRegistrationForm(forms.Form):
    """Form for registering a new tenant/organization."""
    
    organization_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Organization Name',
            'class': 'form-control'
        })
    )
    
    subdomain = forms.SlugField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'subdomain (e.g., mycompany)',
            'class': 'form-control',
            'help_text': 'Lowercase letters, numbers, and hyphens only'
        }),
        help_text='This will be your unique subdomain (e.g., mycompany.yourdomain.com)'
    )
    
    admin_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Admin Email',
            'class': 'form-control'
        })
    )
    
    admin_username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Admin Username',
            'class': 'form-control'
        })
    )
    
    admin_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password (min 8 characters)',
            'class': 'form-control'
        })
    )
    
    confirm_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('admin_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')
        
        return cleaned_data
    
    def clean_subdomain(self):
        subdomain = self.cleaned_data.get('subdomain')
        if subdomain.lower() in ['admin', 'api', 'www', 'mail', 'ftp', 'public']:
            raise forms.ValidationError('This subdomain is reserved. Please choose another.')
        return subdomain.lower()
