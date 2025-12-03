from django import forms
from .models import SolicitacaoReparo, ImagemReparo, InteresseSolicitacao


class SolicitacaoReparoForm(forms.ModelForm):
    """
    Formulário para criar uma nova solicitação de reparo
    """
    class Meta:
        model = SolicitacaoReparo
        fields = ('titulo', 'descricao', 'veiculo')
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Reparo do para-choque dianteiro'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva os danos e o que você precisa',
                'rows': 4
            }),
            'veiculo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Honda Civic 2015'
            }),
        }


class ImagemReparoForm(forms.ModelForm):
    """
    Formulário para upload de imagens de reparo
    """
    class Meta:
        model = ImagemReparo
        fields = ('imagem', 'descricao')
        widgets = {
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Dano frontal do lado direito'
            }),
        }


class InteresseForm(forms.ModelForm):
    """
    Formulário para escritório enviar interesse em uma solicitação
    """
    class Meta:
        model = InteresseSolicitacao
        fields = ('orcamento', 'descricao_proposta')
        widgets = {
            'orcamento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1500.00',
                'step': '0.01'
            }),
            'descricao_proposta': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva sua proposta de reparo',
                'rows': 4
            }),
        }

