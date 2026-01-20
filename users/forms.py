from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Users, UserManager
from rolepermissions.roles import assign_role, clear_roles

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Users, UserManager
from rolepermissions.roles import assign_role, clear_roles

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Usuário ou senha incorretos.",
        'inactive': "Esta conta está inativa.",
    }

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'block w-full rounded-lg border border-slate-300 dark:border-border-dark bg-background-light dark:bg-background-dark py-4 pl-12 pr-4 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-[#58636f] focus:border-primary focus:ring-1 focus:ring-primary sm:text-sm sm:leading-6 h-14',
            'placeholder': 'usuario@exemplo.com',
        })

class UserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'perfil', 'vaga', 'password1', 'password2']


    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas não coincidem.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.vaga = self.cleaned_data["vaga"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perfil'].empty_label = "Selecione um perfil"
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full rounded-md border-0 py-2.5 px-3 text-slate-900 dark:text-white shadow-sm ring-1 ring-inset ring-slate-300 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6 bg-white dark:bg-slate-800',
            })

class UserChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'perfil', 'vaga']

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)

        super().__init__(*args, **kwargs)
        self.fields['perfil'].empty_label = "Selecione um perfil"
        
        # Remover o campo de senha do formulário de edição
        if 'password' in self.fields:
            self.fields.pop('password')

        # Se não for superuser, ocultar perfil
        if not (request_user and request_user.is_superuser):
            self.fields['perfil'].widget = forms.HiddenInput()

        # Aplicar classes CSS a todos os campos
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full rounded-md border-0 py-2.5 px-3 text-slate-900 dark:text-white shadow-sm ring-1 ring-inset ring-slate-300 dark:ring-slate-700 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6 bg-white dark:bg-slate-800',
            })
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        
        clear_roles(user)

        if user.perfil == 'full':
            assign_role(user, 'Full')
        elif user.perfil == 'basic':
            assign_role(user, 'Basic')
        elif user.perfil == 'view':
            assign_role(user, 'ViewOnly')

        if commit:
            user.save()
        return user
