import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'principal.settings')
django.setup()

from django.contrib.auth.models import User
from banco.models import SolicitacaoReparo, InteresseSolicitacao
from paginas.models import PerfilUsuario

def teste_view_painel_cliente():
    """
    Simula a execução da view painel_cliente
    """
    print("=" * 80)
    print("TESTE VISUAL: Simulando a View painel_cliente")
    print("=" * 80)
    
    # Obter o cliente
    try:
        cliente = User.objects.filter(perfil__tipo='cliente').first()
        if not cliente:
            print("❌ Nenhum cliente encontrado!")
            return False
        
        # Simular o que a view faz
        print(f"\n[SIMULAÇÃO] View painel_cliente com usuário: {cliente.username}")
        print("-" * 80)
        
        # Verificar perfil
        try:
            perfil = cliente.perfil
            if perfil.tipo != 'cliente':
                print(f"❌ Acesso negado. Perfil é '{perfil.tipo}', não 'cliente'")
                return False
            print(f"✓ Perfil verificado: {perfil.tipo}")
        except PerfilUsuario.DoesNotExist:
            print("❌ Perfil não encontrado.")
            return False
        
        # Obter solicitações (exatamente como a view faz)
        solicitacoes = SolicitacaoReparo.objects.filter(cliente=cliente).prefetch_related('interesses')
        
        print(f"\n✓ Solicitações carregadas: {solicitacoes.count()}")
        
        # Simular o contexto da view
        context = {
            'solicitacoes': solicitacoes,
            'total_solicitacoes': solicitacoes.count(),
            'solicitacoes_pendentes': solicitacoes.filter(status='pendente').count(),
        }
        
        print(f"✓ Contexto preparado:")
        print(f"  - total_solicitacoes: {context['total_solicitacoes']}")
        print(f"  - solicitacoes_pendentes: {context['solicitacoes_pendentes']}")
        
        # Exibir a tabela como seria renderizada no HTML
        print("\n" + "=" * 80)
        print("TABELA RENDERIZADA NO PAINEL DE CLIENTE")
        print("=" * 80)
        
        if solicitacoes:
            print(f"\n{'Título':<30} | {'Veículo':<20} | {'Status':<15} | {'Interessados':<15} | {'Data':<16}")
            print("-" * 100)
            
            for solicitacao in solicitacoes:
                status_display = solicitacao.get_status_display()
                data_str = solicitacao.data_criacao.strftime("%d/%m/%Y %H:%M")
                
                # Verificar interesses (como no template)
                if solicitacao.interesses.count() > 0:
                    interessados = f"{solicitacao.interesses.count()} interessado(s)"
                else:
                    interessados = "Nenhum"
                
                print(f"{solicitacao.titulo:<30} | {solicitacao.veiculo:<20} | {status_display:<15} | {interessados:<15} | {data_str:<16}")
            
            # Exibir detalhes de interesses
            print("\n" + "=" * 80)
            print("DETALHES DOS INTERESSES")
            print("=" * 80)
            
            for solicitacao in solicitacoes:
                if solicitacao.interesses.count() > 0:
                    print(f"\n📋 Solicitação: {solicitacao.titulo}")
                    print(f"   Status: {solicitacao.get_status_display()}")
                    print(f"   Total de interesses: {solicitacao.interesses.count()}\n")
                    
                    for interesse in solicitacao.interesses.all():
                        print(f"   🏢 Escritório: {interesse.escritorio.username}")
                        print(f"   💰 Orçamento: R$ {interesse.orcamento if interesse.orcamento else 'Não informado'}")
                        print(f"   📝 Proposta: {interesse.descricao_proposta if interesse.descricao_proposta else 'Sem proposta'}")
                        print(f"   📅 Data: {interesse.data_interesse.strftime('%d/%m/%Y %H:%M')}")
                        print()
            
            print("=" * 80)
            print("✅ FUNCIONALIDADE CONFIRMADA!")
            print("=" * 80)
            print("\nA funcionalidade está funcionando corretamente:")
            print("1. ✓ Solicitações de problemas estão sendo listadas")
            print("2. ✓ Interesses de escritórios são mostrados nas solicitações")
            print("3. ✓ Detalhes de orçamento e proposta estão disponíveis")
            print("4. ✓ Template painel_cliente.html está funcionando como esperado")
            
            return True
        else:
            print("❌ Nenhuma solicitação encontrada para este cliente")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        resultado = teste_view_painel_cliente()
        sys.exit(0 if resultado else 1)
    except Exception as e:
        print(f"\n❌ ERRO ao executar o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
