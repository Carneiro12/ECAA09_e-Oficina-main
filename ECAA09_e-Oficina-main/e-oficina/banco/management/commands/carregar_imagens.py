import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from banco.models import Servico

class Command(BaseCommand):
    help = 'Popula Banco de dados com imagens de dados'

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR)
        image_folder = base / 'static' / 'images' / 'danos'

        if not image_folder.exists():
            self.stdout.write(self.style.ERROR(f"Pasta de imagens não encontrada em: {image_folder}"))
            return

        self.stdout.write(f"Procurando imagens em {image_folder}...")

        exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        lista_imagens = [p for p in image_folder.rglob('*') if p.is_file() and p.suffix.lower() in exts]
        self.stdout.write(f"Imagens encontradas: {len(lista_imagens)}")

        inserted = 0
        for caminho in lista_imagens:
            # salvar caminho relativo ao BASE_DIR sem leading slash
            try:
                nome_rel = caminho.relative_to(base).as_posix()
            except Exception:
                nome_rel = caminho.resolve().as_posix()

            if nome_rel.startswith('/'):
                nome_rel = nome_rel[1:]

            # guarda somente o caminho dentro da pasta static, sem "static/" prefix
            if nome_rel.startswith('static/'):
                caminho_db = nome_rel[len('static/'):]   # -> "images/danos/1.jpg"
            else:
                caminho_db = nome_rel

            if Servico.objects.filter(imagem=caminho_db).exists():
                self.stdout.write(self.style.WARNING(f"Servico '{caminho_db}' já existe. Pulando."))
                continue

            try:
                Servico.objects.create(carro=caminho.stem, imagem=caminho_db, tipo='dano')
                inserted += 1
                self.stdout.write(self.style.SUCCESS(f"Produto '{caminho_db}' carregado com sucesso."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao carregar '{caminho_db}': {e}"))

        self.stdout.write(f"Total inseridos: {inserted}")