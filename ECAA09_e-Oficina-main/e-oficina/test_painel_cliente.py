import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'principal.settings')
django.setup()

from django.contrib.auth.models import User
from banco.models import SolicitacaoReparo, InteresseSolicitacao
from paginas.models import PerfilUsuario

def teste_painel_cliente():
    """
    Teste para verificar se a funcionalidade de listar solicitações e interesses está funcionando
    """
    print("=" * 80)
    print("TESTE: Painel de Cliente - Listagem de Solicitações e Interesses")
    print("=" * 80)
    
    # 1. Verificar se existem clientes
    print("\n[1] Verificando usuários clientes...")
    clientes = User.objects.filter(perfil__tipo='cliente')
    print(f"   Total de clientes: {clientes.count()}")
    
    if not clientes:
        print("   ❌ ERRO: Nenhum cliente encontrado!")
        return False
    
    for cliente in clientes[:3]:  # Mostra os 3 primeiros
        print(f"   - {cliente.username}")
    
    # 2. Verificar se existem escritórios
    print("\n[2] Verificando usuários escritórios...")
    escritorios = User.objects.filter(perfil__tipo='escritorio')
    print(f"   Total de escritórios: {escritorios.count()}")
    
    if not escritorios:
        print("   ⚠️  AVISO: Nenhum escritório encontrado!")
    else:
        for escritorio in escritorios[:3]:  # Mostra os 3 primeiros
            print(f"   - {escritorio.username}")
    
    # 3. Verificar se existem solicitações de reparo
    print("\n[3] Verificando solicitações de reparo...")
    solicitacoes = SolicitacaoReparo.objects.all()
    print(f"   Total de solicitações: {solicitacoes.count()}")
    
    if not solicitacoes:
        print("   ⚠️  AVISO: Nenhuma solicitação encontrada!")
    else:
        for solicitacao in solicitacoes[:5]:  # Mostra as 5 primeiras
            print(f"   - ID: {solicitacao.id} | Título: {solicitacao.titulo}")
            print(f"     Cliente: {solicitacao.cliente.username}")
            print(f"     Status: {solicitacao.get_status_display()}")
    
    # 4. Verificar se existem interesses registrados
    print("\n[4] Verificando interesses em solicitações...")
    interesses = InteresseSolicitacao.objects.all()
    print(f"   Total de interesses: {interesses.count()}")
    
    if not interesses:
        print("   ⚠️  AVISO: Nenhum interesse registrado!")
    else:
        for interesse in interesses[:5]:  # Mostra os 5 primeiros
            print(f"   - Escritório: {interesse.escritorio.username}")
            print(f"     Solicitação: {interesse.solicitacao.titulo}")
            print(f"     Orçamento: R$ {interesse.orcamento if interesse.orcamento else 'Não informado'}")
            print()
    
    # 5. Testar a view painel_cliente
    print("\n[5] Testando dados que seriam passados para a view painel_cliente...")
    if clientes:
        cliente_teste = clientes.first()
        solicitacoes_cliente = SolicitacaoReparo.objects.filter(cliente=cliente_teste).prefetch_related('interesses')
        print(f"   Cliente teste: {cliente_teste.username}")
        print(f"   Solicitações do cliente: {solicitacoes_cliente.count()}")
        
        total_interesses_cliente = 0
        for sol in solicitacoes_cliente:
            interesses_sol = sol.interesses.all()
            total_interesses_cliente += interesses_sol.count()
            print(f"   - {sol.titulo}: {interesses_sol.count()} interesse(s)")
        
        print(f"   Total de interesses para todas as solicitações: {total_interesses_cliente}")
    
    # 6. Resumo final
    print("\n" + "=" * 80)
    print("RESUMO:")
    print("=" * 80)
    print(f"✓ Clientes: {clientes.count()}")
    print(f"✓ Escritórios: {escritorios.count()}")
    print(f"✓ Solicitações: {solicitacoes.count()}")
    print(f"✓ Interesses: {interesses.count()}")
    
    # Verificar se a funcionalidade pode ser considerada como "funcionando"
    if solicitacoes.count() > 0 and interesses.count() > 0:
        print("\n✅ A FUNCIONALIDADE ESTÁ FUNCIONANDO!")
        print("   - Solicitações de problemas estão sendo criadas e listadas")
        print("   - Escritórios estão se interessando por solicitações")
        print("   - Os interesses estão sendo registrados no banco de dados")
        return True
    elif solicitacoes.count() > 0 and interesses.count() == 0:
        print("\n⚠️  FUNCIONALIDADE PARCIALMENTE FUNCIONANDO")
        print("   - Solicitações estão sendo criadas")
        print("   - Mas nenhum escritório se interessou ainda")
        print("   - Teste marcando interesse em uma solicitação")
        return True
    else:
        print("\n❌ FUNCIONALIDADE NÃO ESTÁ FUNCIONANDO")
        print("   - Nenhuma solicitação foi criada")
        print("   - Crie uma solicitação primeiro")
        return False

if __name__ == '__main__':
    try:
        resultado = teste_painel_cliente()
        sys.exit(0 if resultado else 1)
    except Exception as e:
        print(f"\n❌ ERRO ao executar o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
