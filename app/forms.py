from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Imię"}), label=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nazwisko"}), label=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}), label=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}), label=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}), label=False)
