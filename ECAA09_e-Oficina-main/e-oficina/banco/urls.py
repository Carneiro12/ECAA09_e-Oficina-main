from django.urls import path
from banco import views

urlpatterns = [
    path("", views.servico_index, name="servico_index"),
    path("<int:servico_id>/", views.servico_detail, name="servico_detail"),
    path("painel/", views.painel_cliente, name="painel_cliente"),
    path("solicitacao-publica/<int:solicitacao_id>/", views.solicitacao_publica, name="solicitacao_publica"),
    path("nova-solicitacao/", views.nova_solicitacao, name="nova_solicitacao"),
    path("solicitacao/<int:solicitacao_id>/", views.editar_solicitacao, name="editar_solicitacao"),
    path("deletar-imagem/<int:imagem_id>/", views.deletar_imagem, name="deletar_imagem"),
    path("deletar-solicitacao/<int:solicitacao_id>/", views.deletar_solicitacao, name="deletar_solicitacao"),
    path("solicitacoes-abertas/", views.listar_solicitacoes_abertas, name="listar_solicitacoes_abertas"),
    path("escritorio/painel/", views.painel_escritorio, name="painel_escritorio"),
    path("marcar-interesse/<int:solicitacao_id>/", views.marcar_interesse, name="marcar_interesse"),
    path("remover-interesse/<int:interesse_id>/", views.remover_interesse, name="remover_interesse"),
]