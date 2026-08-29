from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        # Falha intencional:
        # A API aceita criação de chamados sem título.
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
            },
        }

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]