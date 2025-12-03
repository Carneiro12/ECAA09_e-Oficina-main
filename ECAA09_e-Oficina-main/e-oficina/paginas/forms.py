from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario


class RegistroForm(UserCreationForm):
    """
    Formulário de registro customizado que estende UserCreationForm
    e adiciona campo para escolher tipo de usuário (Cliente ou Escritório)
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    
    tipo = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        label='Tipo de Usuário',
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizar widgets de campos
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
    
    def save(self, commit=True):
        """
        Salva o usuário e cria o perfil associado com o tipo escolhido
        """
        user = super().save(commit=False)
        tipo = self.cleaned_data.get('tipo')
        
        if commit:
            user.save()
            # Criar perfil do usuário com o tipo selecionado
            PerfilUsuario.objects.create(usuario=user, tipo=tipo)
        
        return user
