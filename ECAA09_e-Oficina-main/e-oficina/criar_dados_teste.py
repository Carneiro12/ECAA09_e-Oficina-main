import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'principal.settings')
django.setup()

from django.contrib.auth.models import User
from banco.models import SolicitacaoReparo, InteresseSolicitacao
from paginas.models import PerfilUsuario

def criar_dados_teste():
    """
    Cria dados de teste para verificar a funcionalidade
    """
    print("=" * 80)
    print("CRIANDO DADOS DE TESTE")
    print("=" * 80)
    
    # 1. Criar um escritório (se não existir)
    print("\n[1] Criando usuário escritório...")
    escritorio_user, created = User.objects.get_or_create(
        username='mecanica_teste',
        defaults={
            'email': 'mecanica@teste.com',
            'first_name': 'Mecânica',
            'last_name': 'Teste'
        }
    )
    
    if created:
        escritorio_user.set_password('senha123')
        escritorio_user.save()
        print(f"   ✓ Usuário '{escritorio_user.username}' criado")
    else:
        print(f"   ℹ️  Usuário '{escritorio_user.username}' já existe")
    
    # Criar perfil de escritório
    perfil_escritorio, created_perfil = PerfilUsuario.objects.get_or_create(
        usuario=escritorio_user,
        defaults={'tipo': 'escritorio'}
    )
    
    if created_perfil:
        print(f"   ✓ Perfil de escritório criado para '{escritorio_user.username}'")
    else:
        print(f"   ℹ️  Perfil de escritório já existe para '{escritorio_user.username}'")
    
    # 2. Obter o cliente existente
    print("\n[2] Obtendo usuário cliente...")
    cliente_user = User.objects.filter(perfil__tipo='cliente').first()
    
    if not cliente_user:
        print("   ❌ ERRO: Nenhum cliente encontrado!")
        return False
    
    print(f"   ✓ Cliente encontrado: {cliente_user.username}")
    
    # 3. Criar solicitações de reparo
    print("\n[3] Criando solicitações de reparo...")
    
    solicitacoes_dados = [
        {
            'titulo': 'Reparo de para-choque dianteiro',
            'descricao': 'Para-choque dianteiro danificado em acidente leve. Necessário reparo ou substituição.',
            'veiculo': 'Toyota Corolla 2019'
        },
        {
            'titulo': 'Pintura da lataria',
            'descricao': 'Pintura descascando em várias áreas do carro. Necessário lixar e repintar.',
            'veiculo': 'Honda Civic 2018'
        },
        {
            'titulo': 'Reparo de vidro traseiro',
            'descricao': 'Vidro traseiro trincado. Necessário substituição urgente.',
            'veiculo': 'Ford Fiesta 2020'
        }
    ]
    
    solicitacoes = []
    for dados in solicitacoes_dados:
        solicitacao, created = SolicitacaoReparo.objects.get_or_create(
            cliente=cliente_user,
            titulo=dados['titulo'],
            defaults={
                'descricao': dados['descricao'],
                'veiculo': dados['veiculo'],
                'status': 'pendente'
            }
        )
        solicitacoes.append(solicitacao)
        
        if created:
            print(f"   ✓ Solicitação '{dados['titulo']}' criada")
        else:
            print(f"   ℹ️  Solicitação '{dados['titulo']}' já existe")
    
    # 4. Criar interesses de escritório nas solicitações
    print("\n[4] Criando interesses de escritório...")
    
    for i, solicitacao in enumerate(solicitacoes):
        interesse, created = InteresseSolicitacao.objects.get_or_create(
            solicitacao=solicitacao,
            escritorio=escritorio_user,
            defaults={
                'orcamento': 500.00 + (i * 100),
                'descricao_proposta': f'Posso fazer esse trabalho em 2 dias úteis. Proposta #{i+1}.'
            }
        )
        
        if created:
            print(f"   ✓ Interesse registrado em '{solicitacao.titulo}'")
        else:
            print(f"   ℹ️  Interesse já existe em '{solicitacao.titulo}'")
    
    print("\n" + "=" * 80)
    print("DADOS DE TESTE CRIADOS COM SUCESSO!")
    print("=" * 80)
    return True

if __name__ == '__main__':
    try:
        criar_dados_teste()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERRO ao criar dados de teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
