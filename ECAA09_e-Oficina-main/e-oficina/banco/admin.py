from django.contrib import admin
from .models import Servico, SolicitacaoReparo, ImagemReparo, InteresseSolicitacao


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('carro', 'tipo')
    search_fields = ('carro', 'tipo')


class ImagemReparoInline(admin.TabularInline):
    model = ImagemReparo
    extra = 1


class InteresseInline(admin.TabularInline):
    model = InteresseSolicitacao
    extra = 0
    readonly_fields = ('data_interesse',)


@admin.register(SolicitacaoReparo)
class SolicitacaoReparoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'status', 'data_criacao', 'total_interesses')
    list_filter = ('status', 'data_criacao')
    search_fields = ('titulo', 'cliente__username', 'veiculo')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    inlines = [ImagemReparoInline, InteresseInline]
    
    def total_interesses(self, obj):
        return obj.interesses.count()
    total_interesses.short_description = "Interessados"


@admin.register(ImagemReparo)
class ImagemReparoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'descricao', 'data_upload')
    list_filter = ('data_upload',)
    search_fields = ('solicitacao__titulo', 'descricao')
    readonly_fields = ('data_upload',)


@admin.register(InteresseSolicitacao)
class InteresseAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'escritorio', 'orcamento', 'data_interesse')
    list_filter = ('data_interesse',)
    search_fields = ('solicitacao__titulo', 'escritorio__username')
    readonly_fields = ('data_interesse',)
