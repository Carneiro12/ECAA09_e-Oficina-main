from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from banco.models import Servico, SolicitacaoReparo, ImagemReparo, InteresseSolicitacao
from paginas.models import PerfilUsuario
from .forms import SolicitacaoReparoForm, ImagemReparoForm, InteresseForm


def servico_index(request):
    servicos = Servico.objects.all()
    context = {"servicos": servicos}
    return render(request, "servico_index.html", context)


def servico_detail(request, servico_id):
    servico = Servico.objects.get(id=servico_id)
    context = {"servico": servico}
    return render(request, "servico_detail.html", context)


@login_required(login_url='login')
def painel_cliente(request):
    """
    Painel principal do cliente com suas solicitações e interessados
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'cliente':
            messages.error(request, 'Acesso negado. Este painel é apenas para clientes.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')
    
    solicitacoes = SolicitacaoReparo.objects.filter(cliente=request.user).prefetch_related('interesses')
    context = {
        'solicitacoes': solicitacoes,
        'total_solicitacoes': solicitacoes.count(),
        'solicitacoes_pendentes': solicitacoes.filter(status='pendente').count(),
    }
    return render(request, 'painel_cliente.html', context)


@login_required(login_url='login')
def nova_solicitacao(request):
    """
    View para criar uma nova solicitação de reparo
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'cliente':
            messages.error(request, 'Acesso negado.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SolicitacaoReparoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.cliente = request.user
            solicitacao.save()
            messages.success(request, 'Solicitação criada com sucesso!')
            return redirect('editar_solicitacao', solicitacao_id=solicitacao.id)
    else:
        form = SolicitacaoReparoForm()
    
    context = {'form': form}
    return render(request, 'nova_solicitacao.html', context)


@login_required(login_url='login')
def editar_solicitacao(request, solicitacao_id):
    """
    View para editar uma solicitação, fazer upload de imagens e ver interessados
    """
    solicitacao = get_object_or_404(SolicitacaoReparo, id=solicitacao_id, cliente=request.user)
    
    if request.method == 'POST':
        form = ImagemReparoForm(request.POST, request.FILES)
        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.solicitacao = solicitacao
            imagem.save()
            messages.success(request, 'Imagem enviada com sucesso!')
            return redirect('editar_solicitacao', solicitacao_id=solicitacao.id)
    else:
        form = ImagemReparoForm()
    
    interesses = solicitacao.interesses.all()
    context = {
        'solicitacao': solicitacao,
        'form': form,
        'imagens': solicitacao.imagens.all(),
        'interesses': interesses,
        'total_interesses': interesses.count()
    }
    return render(request, 'editar_solicitacao.html', context)


@login_required(login_url='login')
def deletar_imagem(request, imagem_id):
    """
    View para deletar uma imagem de reparo
    """
    imagem = get_object_or_404(ImagemReparo, id=imagem_id)
    
    # Verificar se o usuário é o dono da solicitação
    if imagem.solicitacao.cliente != request.user:
        messages.error(request, 'Acesso negado.')
        return redirect('painel_cliente')
    
    solicitacao_id = imagem.solicitacao.id
    imagem.delete()
    messages.success(request, 'Imagem deletada com sucesso!')
    return redirect('editar_solicitacao', solicitacao_id=solicitacao_id)


@login_required(login_url='login')
def deletar_solicitacao(request, solicitacao_id):
    """
    View para deletar uma solicitação
    """
    solicitacao = get_object_or_404(SolicitacaoReparo, id=solicitacao_id, cliente=request.user)
    
    if solicitacao.status not in ['pendente', 'cancelado']:
        messages.error(request, 'Só é possível deletar solicitações pendentes ou canceladas.')
        return redirect('painel_cliente')
    
    solicitacao.delete()
    messages.success(request, 'Solicitação deletada com sucesso!')
    return redirect('painel_cliente')


@login_required(login_url='login')
def listar_solicitacoes_abertas(request):
    """
    View para escritório ver todas as solicitações disponíveis
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'escritorio':
            messages.error(request, 'Acesso negado. Este painel é apenas para escritórios.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')
    
    # Mostrar apenas solicitações pendentes
    solicitacoes = SolicitacaoReparo.objects.filter(status='pendente').prefetch_related('imagens', 'interesses')
    
    # Verificar quais o escritório já se interessou
    interesses_ids = InteresseSolicitacao.objects.filter(escritorio=request.user).values_list('solicitacao_id', flat=True)
    
    context = {
        'solicitacoes': solicitacoes,
        'interesses_ids': list(interesses_ids)
    }
    return render(request, 'listar_solicitacoes.html', context)


@login_required(login_url='login')
def painel_escritorio(request):
    """
    Painel para escritórios com a lista de solicitações que o escritório selecionou (interesses).
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'escritorio':
            messages.error(request, 'Acesso negado. Este painel é apenas para escritórios.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')

    # Carregar interesses do escritório juntamente com as solicitações relacionadas
    interesses = InteresseSolicitacao.objects.filter(escritorio=request.user).select_related('solicitacao', 'solicitacao__cliente').prefetch_related('solicitacao__imagens')

    context = {
        'interesses': interesses,
        'total_interesses': interesses.count(),
    }
    return render(request, 'painel_escritorio.html', context)


@login_required(login_url='login')
def solicitacao_publica(request, solicitacao_id):
    """
    View pública para escritórios visualizarem detalhes de uma solicitação
    (permite que a oficina veja imagens, descrição e marque interesse).
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'escritorio':
            messages.error(request, 'Acesso negado. Este painel é apenas para escritórios.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')

    solicitacao = get_object_or_404(SolicitacaoReparo, id=solicitacao_id, status='pendente')

    # Verificar se o escritório já registrou interesse
    existe_interesse = InteresseSolicitacao.objects.filter(solicitacao=solicitacao, escritorio=request.user).first()

    context = {
        'solicitacao': solicitacao,
        'imagens': solicitacao.imagens.all(),
        'interesses': solicitacao.interesses.all(),
        'existe_interesse': existe_interesse is not None,
        'interesse_obj': existe_interesse,
    }
    return render(request, 'solicitacao_detail.html', context)


@login_required(login_url='login')
def marcar_interesse(request, solicitacao_id):
    """
    View para escritório se interessar por uma solicitação
    """
    try:
        perfil = request.user.perfil
        if perfil.tipo != 'escritorio':
            messages.error(request, 'Acesso negado.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('home')
    
    solicitacao = get_object_or_404(SolicitacaoReparo, id=solicitacao_id, status='pendente')
    
    # Verificar se já existe interesse
    interesse_existente = InteresseSolicitacao.objects.filter(
        solicitacao=solicitacao,
        escritorio=request.user
    ).first()
    
    if request.method == 'POST':
        form = InteresseForm(request.POST, instance=interesse_existente)
        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.solicitacao = solicitacao
            interesse.escritorio = request.user
            interesse.save()
            messages.success(request, 'Interesse registrado com sucesso!')
            return redirect('listar_solicitacoes_abertas')
    else:
        form = InteresseForm(instance=interesse_existente)
    
    context = {
        'solicitacao': solicitacao,
        'form': form,
        'existe_interesse': interesse_existente is not None
    }
    return render(request, 'marcar_interesse.html', context)


@login_required(login_url='login')
def remover_interesse(request, interesse_id):
    """
    View para escritório remover seu interesse
    """
    interesse = get_object_or_404(InteresseSolicitacao, id=interesse_id, escritorio=request.user)
    solicitacao_id = interesse.solicitacao.id
    interesse.delete()
    messages.success(request, 'Interesse removido com sucesso!')
    return redirect('listar_solicitacoes_abertas')