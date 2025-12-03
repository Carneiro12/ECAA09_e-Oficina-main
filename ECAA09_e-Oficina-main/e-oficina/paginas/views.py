from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm


def home(request):
    return render(request, "home.html", {})


def login_view(request):
    """
    View para login de usuários
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'login.html', {})


def logout_view(request):
    """
    View para logout de usuários
    """
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')


def registro(request):
    """
    View para registro de novo usuário
    Permite escolher entre Cliente ou Escritório
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            tipo_usuario = form.cleaned_data.get('tipo')
            tipo_display = dict(form.fields['tipo'].choices)[tipo_usuario]
            
            messages.success(
                request, 
                f'Registro realizado com sucesso! Bem-vindo, {user.username}! Você está registrado como {tipo_display}.'
            )
            return redirect('home')
        else:
            # Se houver erros no formulário, exibi-los
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistroForm()
    
    context = {
        'form': form,
        'page_title': 'Registro'
    }
    return render(request, 'registro.html', context)